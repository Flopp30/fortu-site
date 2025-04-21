from typing import Annotated

from pydantic import Field, BeforeValidator

from fortu_site.config.utils import (
    BaseFromEnvConfig,
    env_to_abs_path,
    split_string_from_env,
)


class DatabaseConfig(BaseFromEnvConfig):
    host: str = Field(..., alias='DB_HOST')
    port: int = Field(..., alias='DB_PORT')
    user: str = Field(..., alias='DB_USER')
    password: str = Field(..., alias='DB_PASSWORD')
    database: str = Field(..., alias='DB_NAME')
    echo: bool = Field(False, alias='DB_ECHO')
    cache_size: int = Field(0, alias='DB_CACHE_SIZE')
    pool_size: int = Field(10, alias='DB_POOL_SIZE')

    @property
    def full_url(self) -> str:
        return f'postgresql+asyncpg://{self.user}:{self.password}@{self.host}:{self.port}/{self.database}'


class LoggingConfig(BaseFromEnvConfig):
    level: str = Field('INFO', alias='LOGGING_LEVEL')
    file_dir: Annotated[str | None, BeforeValidator(env_to_abs_path)] = Field('./logs', alias='LOGGING_FILE_DIR')
    file_name: str = Field('fortu-site.log', alias='LOGGING_FILE_NAME')
    log_format: str = Field(
        '%(asctime)s - %(name)s - %(levelname)s - [%(filename)s:%(lineno)d] - %(message)s',
        alias='LOGGING_FORMAT',
    )
    console_log_enabled: bool = Field(True, alias='LOGGING_CONSOLE_LOG_ENABLED')


class WebConfig(BaseFromEnvConfig):
    templates_dir: Annotated[str, BeforeValidator(env_to_abs_path)] = Field('./templates/', alias='WEB_TEMPLATES_DIR')
    static_dir: Annotated[str, BeforeValidator(env_to_abs_path)] = Field('./static/', alias='WEB_FILES_STATIC_DIR')
    static_path: str = Field('/static/', alias='WEB_STATIC_PATH')


class ApiConfig(BaseFromEnvConfig):
    cors_origins: Annotated[list[str], BeforeValidator(split_string_from_env)] = Field(['*'], alias='API_CORS_ORIGINS')
    allow_headers: Annotated[list[str], BeforeValidator(split_string_from_env)] = Field(
        ['*'], alias='API_ALLOW_HEADERS'
    )
    allow_methods: Annotated[list[str], BeforeValidator(split_string_from_env)] = Field(
        ['*'], alias='API_ALLOW_METHODS'
    )


class AuthConfig(BaseFromEnvConfig):
    session_ttl_sec: int = Field(60 * 60, alias='AUTH_SESSION_TTL_SEC')
