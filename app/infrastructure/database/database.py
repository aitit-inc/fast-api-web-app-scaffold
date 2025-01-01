"""Database module."""

import glob
import logging
from contextlib import asynccontextmanager
from pathlib import Path
from typing import AsyncGenerator, Any

import asyncpg
from asyncpg import Connection
from sqlalchemy.ext.asyncio import async_sessionmaker, AsyncSession
from sqlalchemy.ext.asyncio import create_async_engine, AsyncEngine
from sqlalchemy.orm import declarative_base
from sqlalchemy.sql import select, func, text
from sqlmodel import SQLModel

logger = logging.getLogger(__name__)

Base = declarative_base()


class Database:
    """Database class."""

    def __init__(self, db_url: str, echo: bool = False) -> None:
        self._dsn: str = db_url
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

    # TODO: Delete this method
    async def create_db_and_tables(self, init_db: bool) -> None:
        """Create database and tables."""
        if not init_db:
            logger.info("Skipping db creation because init_db is False")
            return

        async with self._engine.begin() as conn:
            await conn.run_sync(SQLModel.metadata.create_all)

    async def load_seeds(self, init_db: bool) -> None:
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

            # Use asyncpg to execute the COPY statement asynchronously
            dsn = self._dsn.replace('postgresql+asyncpg', 'postgresql')
            import_csv_conn: Connection[Any] = await asyncpg.connect(dsn)
            try:
                # Use copy_from to import the data
                await import_csv_conn.copy_to_table(
                    table_name=table_name,
                    # source=csv_data.encode('utf-8'),
                    source=csv_file,
                    format='csv',
                    delimiter=',',
                    header=True,
                )
            finally:
                await import_csv_conn.close()

        seed_files = glob.glob('db/data/seed/*.csv')
        for seed_file in seed_files:
            logger.info("Importing seed file: %s", seed_file)
            await import_csv(Path(seed_file))

        auto_increment_tables = [
            'sample_items'
        ]
        async with self._engine.connect() as connection:
            for table in auto_increment_tables:
                count_query = select(func.count()).select_from(
                    text(table))
                record_count = (await connection.execute(count_query)).scalar()
                logger.info(f'record_count of {table}: {record_count}')

                if record_count is None or record_count == 0:
                    logger.info(f'Skipping {table} because it has no records')
                    continue

                await connection.execute(
                    text(
                        f'ALTER SEQUENCE {table}_id_seq RESTART WITH '
                        f'{record_count + 1};'))
                await connection.commit()
