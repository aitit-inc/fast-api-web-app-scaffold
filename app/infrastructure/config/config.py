"""Settins for the app."""
import logging
from datetime import datetime
from typing import Callable
from zoneinfo import ZoneInfo

from pydantic_settings import BaseSettings


# TODO: Try lru_cache
# ref: https://fastapi.tiangolo.com/advanced/settings/#creating-the-settings-only-once-with-lru_cache


class Settings(BaseSettings):
    """Settings for the app."""
    app_name: str = "FastAPI web app scaffold"

    # TODO: Delete this.
    timezone_str: str = 'UTC'

    # db
    db_dsn: str = 'sqlite:///./test.db'
    echo_sql: bool = False
    init_db_on_startup: bool = False

    # noinspection PyDataclass
    origins: list[str] = ['*']
    log_level_str: str = 'INFO'

    @property
    def log_level(self) -> int:
        """Get log level."""
        if self.log_level_str == 'DEBUG':
            return logging.DEBUG
        elif self.log_level_str == 'INFO':
            return logging.INFO
        elif self.log_level_str == 'WARNING':
            return logging.WARNING
        elif self.log_level_str == 'ERROR':
            return logging.ERROR
        elif self.log_level_str == 'CRITICAL':
            return logging.CRITICAL
        else:
            raise ValueError(f'Invalid log level: {self.log_level_str}')

    # TODO: Delete this.
    @property
    def timezone(self) -> ZoneInfo:
        """Get timezone."""
        return ZoneInfo(self.timezone_str)

    @property
    def get_now(self) -> Callable[[], datetime]:
        """Get now function."""
        return lambda: datetime.now(self.timezone)

    class Config:
        """meta"""
        env_file = './app/.env'
        env_file_encoding = 'utf-8'


def get_settings() -> Settings:
    """Get settings."""
    return Settings()
