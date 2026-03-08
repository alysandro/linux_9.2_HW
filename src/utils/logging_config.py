import logging
import logging.handlers
from pathlib import Path
import sys
from typing import Literal

import colorlog
from decouple import config  # comment for test ok - import json_log_formatter

from src.utils.constants import (
    DEFAULT_BACKUP_COUNT,
    DEFAULT_LOG_FORMAT,
    DEFAULT_LOG_LEVEL,
    MAX_LOG_SIZE,  # исправлена опечатка в имени константы
)


# 1. Определяем корень проекта
ROOT_DIR = Path(__file__).parent.parent.parent
LOGS_DIR = ROOT_DIR / 'logs'
LOGS_DIR.mkdir(exist_ok=True)
LogLevel = Literal['DEBUG', 'INFO', 'WARNING', 'ERROR', 'CRITICAL']


def get_log_level(level_str: str) -> int:
    """Преобразует строку уровня логирования в числовой код."""
    level_name = level_str.upper()
    valid_levels = {
        'DEBUG': logging.DEBUG,
        'INFO': logging.INFO,
        'WARNING': logging.WARNING,
        'ERROR': logging.ERROR,
        'CRITICAL': logging.CRITICAL,
    }
    if level_name in valid_levels:
        return valid_levels[level_name]
    raise ValueError(f'Неизвестный уровень логирования: {level_name}')


def validate_log_format(log_format: str, valid_formats: list[str]) -> None:
    """Проверяет формат логов на соответствие допустимым значениям."""
    if log_format not in valid_formats:
        error_msg = f'Недопустимый формат логов: {log_format}. Используйте: {", ".join(valid_formats)}.'
        temp_logger = logging.getLogger(__name__)
        temp_logger.error(error_msg)
        raise RuntimeError('Не удалось настроить логирование из‑за некорректного формата логов')


# 2. Загружаем настройки из .env с fallback к константам
try:
    # Пути
    LOG_FILE: Path = LOGS_DIR / config('LOG_FILE', default='app.log')
    DATA_DIR: Path = ROOT_DIR / config('DATA_DIR', default='data')

    # Уровни логирования
    LOG_LEVEL_FILE: int = get_log_level(config('LOG_LEVEL_FILE', default=DEFAULT_LOG_LEVEL))
    LOG_LEVEL_CONSOLE: int = get_log_level(config('LOG_LEVEL_CONSOLE', default=DEFAULT_LOG_LEVEL))

    # Ротация логов
    LOG_MAX_SIZE: int = config('LOG_MAX_SIZE', default=MAX_LOG_SIZE, cast=int)
    LOG_BACKUP_COUNT: int = config('LOG_BACKUP_COUNT', default=DEFAULT_BACKUP_COUNT, cast=int)

    # Формат логов
    LOG_FORMAT: str = config('LOG_FORMAT', default=DEFAULT_LOG_FORMAT).lower()

except Exception:
    temp_logger = logging.getLogger(__name__)
    temp_logger.exception('Ошибка загрузки конфигурации логгера')  # убрана передача e
    raise  # повторно выбрасываем исключение


# 3. Настраиваем логгер
def setup_logger(
    name: str = 'app_logger',
    log_file: Path | None = None,
    level_file: int | None = None,
    level_console: int | None = None,
    format_type: str | None = None,
) -> logging.Logger:
    logger = logging.getLogger(name)

    if logger.handlers:
        return logger

    file_level = level_file or LOG_LEVEL_FILE
    console_level = level_console or LOG_LEVEL_CONSOLE
    log_format = format_type or LOG_FORMAT
    log_file = log_file or LOG_FILE

    logger.setLevel(logging.DEBUG)

    # Форматировщики
    if log_format == 'json':
        formatter = json_log_formatter.JSONFormatter()
    elif log_format == 'color':
        formatter = colorlog.ColoredFormatter(
            '%(log_color)s%(asctime)s | %(levelname)-8s | %(name)s:%(lineno)d | %(reset)s %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S',
            log_colors={
                'DEBUG': 'cyan',
                'INFO': 'green',
                'WARNING': 'yellow',
                'ERROR': 'red',
                'CRITICAL': 'red,bg_white',
            },
        )
    else:  # plain
        formatter = logging.Formatter(
            '%(asctime)s | %(levelname)-8s | %(name)s:%(lineno)d | %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S',
        )

    # Handler для файла (с ротацией)
    file_handler = logging.handlers.RotatingFileHandler(
        filename=log_file,
        maxBytes=LOG_MAX_SIZE,
        backupCount=LOG_BACKUP_COUNT,
        encoding='utf-8',
    )
    file_handler.setLevel(file_level)
    file_handler.setFormatter(formatter)

    # Handler для консоли
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(console_level)
    console_handler.setFormatter(formatter)

    logger.addHandler(file_handler)
    logger.addHandler(console_handler)

    return logger


# Экспортируем готовый логгер
logger = setup_logger()
