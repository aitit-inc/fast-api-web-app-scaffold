"""Load seeds."""
import asyncio
import logging
import os
import sys

import click

# NEED this when executing this file from other directory.
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.config import get_settings, \
    get_settings_for_testing
from app.infrastructure.database.database import Database

logger = logging.getLogger('uvicorn')


async def load_seeds(test: bool) -> None:
    """Load seeds."""
    logger.info("Loading seeds...")
    config = get_settings_for_testing() if test else get_settings()
    db = Database(
        db_url=config.db_dsn,
        echo=config.echo_sql,
        seed_dir=config.seed_dir,
    )
    await db.load_seeds(init_db=True)
    await db.adjust_all_sequences()


@click.command()
@click.option('--test', is_flag=True, help="Run load_seeds in test mode.")
def main(test: bool) -> None:
    """Load seeds."""
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    logging.basicConfig(level=logging.INFO)
    logging.getLogger('uvicorn').setLevel(logging.INFO)
    logger.info("Executing the load_seeds script.")
    asyncio.run(load_seeds(test))
    logger.info("Finished executing the load_seeds script.")


if __name__ == '__main__':
    main()
