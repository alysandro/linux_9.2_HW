from typing import Final


# Константы — допустимые значения, которые не меняются
VALID_LOG_FORMATS: Final[set[str]] = {'color', 'json', 'plain'}
DEFAULT_LOG_FORMAT: Final[str] = 'color'
DEFAULT_LOG_LEVEL: Final[str] = 'INFO'
MAX_LOG_SIZE: Final[int] = 10 * 1024 * 1024  # 10 МБ
DEFAULT_BACKUP_COUNT: Final[int] = 5
