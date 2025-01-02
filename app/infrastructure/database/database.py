"""Database module."""

import glob
import logging
from contextlib import asynccontextmanager
from pathlib import Path
from typing import AsyncGenerator, Any

import asyncpg
from asyncpg import Connection
from sqlalchemy.ext.asyncio import async_sessionmaker, AsyncSession, \
    create_async_engine, AsyncEngine
from sqlalchemy.orm import declarative_base

logger = logging.getLogger(__name__)

Base = declarative_base()


class Database:
    """Database class."""

    def __init__(
            self,
            db_url: str,
            echo: bool = False,
            seed_dir: str = 'db/data/seed',
    ) -> None:
        self._dsn: str = db_url
        self._seed_dir: Path = Path(seed_dir)
        self._engine = create_async_engine(db_url, echo=echo, future=True)

        self._session_factory = async_sessionmaker(
            bind=self._engine,
            autocommit=False,
            autoflush=False,
            expire_on_commit=False,
        )

    def get_engine(self) -> AsyncEngine:
        """Get engine."""
        return self._engine

    @asynccontextmanager
    async def session(self) -> AsyncGenerator[AsyncSession, None]:
        """Async session context manager."""
        try:
            async with self._session_factory() as session:
                yield session
        except Exception:
            logger.exception("Session rollback because of exception")
            await session.rollback()
            raise

    async def load_seeds(
            self,
            init_db: bool,
    ) -> None:
        """Load seeds."""
        if not init_db:
            logger.info("Skipping seed loading because init_db is False")
            return

        async def import_csv(csv_file: Path) -> None:
            """Import a CSV file into the database using asyncpg."""
            table_name = csv_file.stem
            if table_name == 'user':
                # 'user' is a reserved word, so it is enclosed in quotes
                table_name = '"user"'

            # Read the file
            with open(csv_file, 'r', encoding='utf-8') as fp:
                csv_data = fp.read()
                column_names = csv_data.split('\n')[0].split(',')

            dsn = self._dsn.replace('+asyncpg', '')
            import_csv_conn: Connection[Any] = await asyncpg.connect(dsn)
            try:
                # Use copy_from to import the data
                await import_csv_conn.copy_to_table(
                    table_name=table_name,
                    source=csv_file,
                    columns=column_names,
                    format='csv',
                    delimiter=',',
                    header=True,
                )
            finally:
                await import_csv_conn.close()

        seed_files = glob.glob(str(self._seed_dir / '*.csv'))
        for seed_file in seed_files:
            logger.info("Importing seed file: %s", seed_file)
            await import_csv(Path(seed_file))
