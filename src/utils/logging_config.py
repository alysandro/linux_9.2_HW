import logging
import logging.handlers
from pathlib import Path
import sys
from typing import Literal

from src.utils.constants import (
    LOGS_DIR,
)


# 1. Сначала определяем уровни логирования (можно добавить загрузку из .env позже)
LOG_LEVEL_FILE = logging.DEBUG
LOG_LEVEL_CONSOLE = logging.INFO

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


def setup_logger(
    name: str = 'app_logger',
    log_file: Path | None = None,
    level_file: int | None = None,
    level_console: int | None = None,
    mode: str = 'w',  # По умолчанию 'w' для ДЗ, но можно передать 'a'
) -> logging.Logger:
    """Универсальный логгер с гибкими настройками."""
    logger = logging.getLogger(name)

    if logger.handlers:
        return logger

    logger.setLevel(logging.DEBUG)

    # 1. ПУТЬ: Если файл не передан, создаем его в LOGS_DIR по имени логгера
    final_log_file = log_file or (LOGS_DIR / f'{name}.log')

    # 2. ФОРМАТ (из констант или ТЗ)
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s', datefmt='%Y-%m-%d %H:%M:%S')

    # 3. ФАЙЛОВЫЙ ОБРАБОТЧИК
    # Используем level_file (если передан) или глобальный LOG_LEVEL_FILE из .env
    file_handler = logging.FileHandler(final_log_file, mode=mode, encoding='utf-8')
    file_handler.setFormatter(formatter)
    file_handler.setLevel(level_file if level_file is not None else LOG_LEVEL_FILE)

    # 4. КОНСОЛЬНЫЙ ОБРАБОТЧИК
    # Используем level_console или глобальный LOG_LEVEL_CONSOLE из .env
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setFormatter(formatter)
    console_handler.setLevel(level_console if level_console is not None else LOG_LEVEL_CONSOLE)

    logger.addHandler(file_handler)
    logger.addHandler(console_handler)

    return logger
