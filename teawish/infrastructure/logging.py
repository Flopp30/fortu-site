import logging
import os
from logging.handlers import TimedRotatingFileHandler

from teawish.config import LoggingConfig


log = logging.getLogger(__name__)


def setup_logging():
    log_config: LoggingConfig = LoggingConfig.from_env()
    formatter: logging.Formatter = logging.Formatter(log_config.log_format)

    root_logger = logging.getLogger()
    root_logger.setLevel(log_config.level)

    if log_config.console_log_enabled:
        console_handler = logging.StreamHandler()
        root_logger.addHandler(console_handler)

    if log_config.file_dir:
        log_path: str = log_config.file_dir
        os.makedirs(log_path, exist_ok=True)
        log_file: str = os.path.join(log_path, log_config.file_name)

        timed_handler = TimedRotatingFileHandler(
            log_file,
            when='midnight',
            interval=1,
            backupCount=5,
            encoding='utf-8',
        )
        root_logger.addHandler(timed_handler)

        # Создаем путь для файла ошибок
        error_log_file = os.path.join(log_path, f'errors_{log_config.file_name}')
        # Обработчик для ошибок
        error_handler = TimedRotatingFileHandler(
            error_log_file,
            when='midnight',
            interval=1,
            backupCount=10,  # Для ошибок храним дольше - 10 дней
            encoding='utf-8',
        )
        error_handler.setLevel(logging.ERROR)
        root_logger.addHandler(error_handler)

    for handler in root_logger.handlers:
        handler.setFormatter(formatter)
        if not isinstance(handler, TimedRotatingFileHandler) or handler.level == logging.NOTSET:
            handler.setLevel(log_config.level)

    log.info('Logging is configured')
