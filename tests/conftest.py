"""Pytest configuration file for the trainer_manager app."""
import asyncio
import os
import time

import pytest
from dotenv import load_dotenv
from pytest import Config


# pylint: disable=unused-argument
def pytest_configure(config: Config) -> None:
    """Pytest configuration hook.

    Can be used to configure the pytest session.
    """
    print("Initializing resources...")

    timezone = 'UTC'
    print(f'Setting timezone to {timezone}')
    os.environ['TZ'] = timezone
    time.tzset()  # Set the timezone

    # Load environment variables from .env.test file
    load_dotenv(dotenv_path='app/.env.test', override=True)
    # [NOTE]: This print is required to ensure they are loaded to env.
    print('os.environ: ', os.environ)


@pytest.fixture(scope="session")
def event_loop():  # type: ignore
    """Create a single event loop for all tests."""
    loop = asyncio.new_event_loop()
    yield loop
    loop.close()
