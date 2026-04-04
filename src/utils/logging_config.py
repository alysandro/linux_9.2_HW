from dataclasses import dataclass
import logging
from logging import LogRecord
import logging.handlers
from pathlib import Path
import sys
from typing import ClassVar, Literal

from src.utils.constants import (
    DEFAULT_BACKUP_COUNT,
    DEFAULT_LOG_FORMAT,
    LOG_FORMATS_CONFIG,
    LOG_LEVELS,
    LOGS_DIR,
    MAX_LOG_SIZE,
    VALID_LOG_FORMATS,
)


LogLevel = Literal['DEBUG', 'INFO', 'WARNING', 'ERROR', 'CRITICAL']
LogFormat = Literal['color', 'json', 'plain']


@dataclass
class LoggerConfig:
    name: str = 'app_logger'
    log_file: Path | None = None
    level_file: LogLevel | None = None
    level_console: LogLevel | None = None
    log_format: LogFormat | str = DEFAULT_LOG_FORMAT
    mode: str = 'a'  # 'a' — дописываем, 'w' — перезаписываем
    use_module_name: bool = True  # флаг: использовать имя модуля для имени файла
    module_name_template: str = '{module}.log'  # шаблон имени файла


def get_log_level(level_str: str) -> int:
    """Преобразует строку уровня логирования в числовой код."""
    level_name = level_str.upper()
    if level_name not in LOG_LEVELS:
        raise ValueError(f'Неизвестный уровень логирования: {level_name}')
    return LOG_LEVELS[level_name]


def validate_log_format(log_format: str) -> None:
    """Проверяет формат логов на соответствие допустимым значениям."""
    if log_format not in VALID_LOG_FORMATS:
        error_msg = f'Недопустимый формат логов: {log_format}. Используйте: {", ".join(VALID_LOG_FORMATS)}.'
        temp_logger = logging.getLogger(__name__)
        temp_logger.error(error_msg)
        raise RuntimeError('Не удалось настроить логирование из‑за некорректного формата логов')


class ColorFormatter(logging.Formatter):
    """Форматировщик с цветным выводом для консоли."""

    COLORS: ClassVar[dict[str, str]] = {
        'DEBUG': '\033[36m',  # Cyan
        'INFO': '\033[32m',  # Green
        'WARNING': '\033[33m',  # Yellow
        'ERROR': '\033[31m',  # Red
        'CRITICAL': '\033[35m',  # Magenta
    }
    RESET: ClassVar[str] = '\033[0m'

    def format(self, record: LogRecord) -> str:
        log_message = super().format(record)
        levelname = record.levelname
        if levelname in self.COLORS:
            return f'{self.COLORS[levelname]}{log_message}{self.RESET}'
        return log_message


def setup_logger(config: LoggerConfig | None = None) -> logging.Logger:
    """Универсальный логгер с гибкими настройками.
    :rtype: logging.Logger
    """
    if config is None:
        config = LoggerConfig()
    # Валидация формата
    validate_log_format(config.log_format)

    logger = logging.getLogger(config.name)
    if logger.handlers:  # Уже настроен
        return logger

    # Уровни логирования
    file_level = get_log_level(config.level_file or 'DEBUG')
    console_level = get_log_level(config.level_console or 'INFO')

    # Форматировщик
    formatter: logging.Formatter
    if config.log_format == 'color':
        formatter = ColorFormatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s', datefmt='%Y-%m-%d %H:%M:%S')
    else:
        formatter = logging.Formatter(
            LOG_FORMATS_CONFIG.get(config.log_format, LOG_FORMATS_CONFIG['plain']), datefmt='%Y-%m-%d %H:%M:%S'
        )

    # Путь к файлу (новый блок)
    if config.log_file is not None:
        final_log_file = config.log_file
    elif config.use_module_name:
        module_part = config.name.split('.')[-1]
        filename = config.module_name_template.format(module=module_part)
        final_log_file = LOGS_DIR / filename
    else:
        final_log_file = LOGS_DIR / f'{config.name}.log'

    # Файловый обработчик с ротацией
    file_handler = logging.handlers.RotatingFileHandler(
        final_log_file, maxBytes=MAX_LOG_SIZE, backupCount=DEFAULT_BACKUP_COUNT, encoding='utf-8', mode=config.mode
    )
    file_handler.setFormatter(formatter)
    file_handler.setLevel(file_level)

    # Консольный обработчик
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setFormatter(formatter)
    console_handler.setLevel(console_level)

    logger.setLevel(logging.DEBUG)  # Общий уровень DEBUG
    logger.addHandler(file_handler)
    logger.addHandler(console_handler)

    return logger


def get_module_logger(module_name: str) -> logging.Logger:
    """Создаёт логгер для модуля по его имени.

    Args:
        module_name (str): имя модуля (например, 'masks', 'json_reader')

    Returns:
        logging.Logger: настроенный логгер
    """
    config = LoggerConfig(name=module_name, use_module_name=True, module_name_template='{module}.log')
    return setup_logger(config)
