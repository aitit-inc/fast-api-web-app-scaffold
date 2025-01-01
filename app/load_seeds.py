import os
import sys
import logging

# Need this when executing this file from other directory.
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.container import Container


logger = logging.getLogger('uvicorn')

async def load_seeds() -> None:
    logger.info("Starting the load_seeds function...")
    container = Container()
    _db = container.db()
    await _db.load_seeds(init_db=True)


if __name__ == '__main__':
    import asyncio

    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    logging.basicConfig(level=logging.INFO)
    logging.getLogger('uvicorn').setLevel(logging.INFO)
    logger.info("Executing the load_seeds script.")
    asyncio.run(load_seeds())
    logger.info("Finished executing the load_seeds script.")
