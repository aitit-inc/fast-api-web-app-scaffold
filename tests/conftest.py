"""Pytest configuration file for the trainer_manager app."""
import os
import time

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
    load_dotenv(dotenv_path='app/.env.test')

    # Set test DB DSN
    os.environ['DB_DSN'] = os.getenv('DB_DSN', 'default_dsn_value')
