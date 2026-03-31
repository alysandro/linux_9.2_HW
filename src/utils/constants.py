import logging
from pathlib import Path
from typing import Final


# Вычисляем корень проекта относительно этого файла (constants.py -> utils -> src -> корень)
ROOT_DIR = Path(__file__).resolve().parent.parent.parent
LOGS_DIR = ROOT_DIR / 'logs'
DATA_DIR = ROOT_DIR / 'data'

# Создаем папки сразу, чтобы потом не ловить ошибки
LOGS_DIR.mkdir(exist_ok=True, parents=True)
DATA_DIR.mkdir(exist_ok=True, parents=True)


# Константы — допустимые значения, которые не меняются
VALID_LOG_FORMATS: Final[set[str]] = {'color', 'json', 'plain'}
DEFAULT_LOG_FORMAT: Final[str] = 'color'
DEFAULT_LOG_LEVEL: Final[str] = 'DEBUG'
MAX_LOG_SIZE: Final[int] = 10 * 1024 * 1024  # 10 МБ
DEFAULT_BACKUP_COUNT: Final[int] = 5

# Уровни логирования — строковые константы
LOG_LEVELS: Final[dict[str, int]] = {
    'DEBUG': logging.DEBUG,
    'INFO': logging.INFO,
    'WARNING': logging.WARNING,
    'ERROR': logging.ERROR,
    'CRITICAL': logging.CRITICAL,
}

# Форматы логов
LOG_FORMATS_CONFIG: Final[dict[str, str]] = {
    'plain': '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    'json': '{"time": "%(asctime)s", "logger": "%(name)s", "level": "%(levelname)s", "message": "%(message)s"}',
}
