"""Settins for the app."""
import logging
from datetime import datetime
from typing import Callable
from zoneinfo import ZoneInfo

from pydantic_settings import BaseSettings

from app.interfaces.middlewares.authorizer import AuthMethod


# TODO: Try lru_cache
# ref: https://fastapi.tiangolo.com/advanced/settings/#creating-the-settings-only-once-with-lru_cache


class Settings(BaseSettings):
    """Settings for the app."""
    app_name: str = "FastAPI web app scaffold"
    timezone_str: str = 'UTC'

    # db
    db_dsn: str = 'sqlite:///./test.db'
    echo_sql: bool = False
    init_db_on_startup: bool = False
    seed_dir: str = './db/data/seed'

    # noinspection PyDataclass
    origins: list[str] = ['*']
    log_level_str: str = 'INFO'

    # auth
    auth_method: AuthMethod = AuthMethod.SESSION_COOKIE

    # session cookie auth
    login_session_secret_key: str = 'you_must_change_this_key'
    login_session_expire_minutes: int = 60 * 24 * 7
    login_session_cookie_name: str = 'session'
    login_session_cookie_secure: bool = True
    login_session_cookie_httponly: bool = True
    login_session_cookie_samesite: str = 'lax'

    # token auth
    issuer: str = 'https://fawapp.com'
    audience: str = 'https://fawapp.com'
    access_token_expire_minutes: int = 30
    refresh_token_expire_minutes: int = 60 * 24 * 7
    token_secret_key: str = 'you_must_change_this_key'
    token_algorithm: str = 'HS256'

    # FOR TEST ONLY
    pass_hash_for_test: str = 'pass_hash_for_test_auth'

    @property
    def log_level(self) -> int:
        """Get log level."""
        if self.log_level_str == 'DEBUG':
            return logging.DEBUG
        if self.log_level_str == 'INFO':
            return logging.INFO
        if self.log_level_str == 'WARNING':
            return logging.WARNING
        if self.log_level_str == 'ERROR':
            return logging.ERROR
        if self.log_level_str == 'CRITICAL':
            return logging.CRITICAL
        raise ValueError(f'Invalid log level: {self.log_level_str}')

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


def get_settings_for_testing() -> Settings:
    """Get settings for testing."""
    return Settings(_env_file='./app/.env.test')  # type: ignore
