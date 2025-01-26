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

            def _get_table_name(csv_file: Path) -> str:
                _, table_name_ = csv_file.stem.split('_', 1)
                return table_name_

            table_name = _get_table_name(csv_file)
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

        seed_files = sorted(glob.glob(str(self._seed_dir / '*.csv')))
        for seed_file in seed_files:
            logger.info('Importing seed file: %s', seed_file)
            await import_csv(Path(seed_file))

    async def _reset_sequence(
            self, table_name: str, id_column: str = 'id') -> None:
        """Adjust the auto-increment sequence for a table."""
        dsn = self._dsn.replace('+asyncpg', '')
        reset_conn: Connection[Any] = await asyncpg.connect(dsn)
        try:
            # Get the maximum id value from the table
            max_id_query = f'SELECT MAX({id_column}) FROM {table_name}'
            max_id_row = await reset_conn.fetchrow(max_id_query)

            # Default to 0 if table is empty
            max_id = max_id_row[0] or 0  # type: ignore

            # Reset the sequence to max_id + 1
            sequence_name = f'{table_name}_{id_column}_seq'
            reset_sequence_query = \
                f"SELECT setval('{sequence_name}', $1, false)"
            await reset_conn.execute(reset_sequence_query, max_id + 1)

        finally:
            await reset_conn.close()

    async def adjust_all_sequences(self) -> None:
        """Adjust all sequences after loading seeds."""
        table_names = [
            ('users', 'id'),
            ('roles', 'id'),
            ('permissions', 'id'),
            ('sample_items', 'id'),
        ]
        for table_name, id_col in table_names:
            logger.info('adjust sequence of %s', table_name)
            await self._reset_sequence(table_name, id_column=id_col)
