import json
from pathlib import Path
from typing import Any

import pandas as pd

from src.utils.constants import DATA_DIR
from src.utils.logging_config import get_module_logger


logger = get_module_logger('file_loader')


def _validate_file(path: Path, valid_extensions: list[str]) -> bool:
    """
    Проверяет существование файла и его расширение.

    Args:
        path: Путь к файлу.
        valid_extensions: Список допустимых расширений (например, ['.csv']).
    Returns:
        True, если файл существует и имеет допустимое расширение, иначе False.
    """
    if not path.exists() or not path.is_file():
        logger.error('Файл не найден или не является файлом: %s', path)
        return False

    if path.suffix.lower() not in valid_extensions:
        logger.error(
            'Ошибка: Файл %s имеет неверное расширение. Ожидалось: %s', path.name, ', '.join(valid_extensions)
        )
        return False

    return True


def _normalize_dict_keys(data: list[dict[Any, Any]]) -> list[dict[str, Any]]:
    """Приводит ключи всех словарей в списке к типу str."""
    return [{str(k): v for k, v in item.items()} for item in data]


def load_transactions_from_csv(file_name: str) -> list[dict[str, Any]]:
    """Загружает транзакции из CSV‑файла в папке DATA_DIR."""
    csv_path = DATA_DIR / file_name

    if not _validate_file(csv_path, ['.csv']):
        return []

    try:
        logger.info('Читаем файл: %s', csv_path.name)
        csv_df = pd.read_csv(csv_path, sep=None, engine='python')
        logger.info('Успешно прочитано %s транзакций из %s', len(csv_df), csv_path.name)

        # Нормализуем ключи к str
        data = csv_df.to_dict('records')
        return _normalize_dict_keys(data)

    except pd.errors.EmptyDataError:
        logger.exception('CSV‑файл пуст: %s', csv_path.name)
        return []

    except pd.errors.ParserError:
        logger.exception('Ошибка парсинга CSV: %s', csv_path.name)
        return []

    except PermissionError:
        logger.exception('Нет доступа к файлу: %s', csv_path)
        return []
    except Exception:
        logger.exception('Неожиданная ошибка при чтении CSV: %s', csv_path.name)
        return []


def read_transactions_from_json(file_path: str) -> list[dict[str, Any]]:
    """Читает JSON‑файл с транзакциями и возвращает список словарей."""
    path = Path(file_path)

    if not _validate_file(path, ['.json']):
        return []

    try:
        with path.open('r', encoding='utf-8') as file:
            data = json.load(file)

        if not isinstance(data, list):
            logger.error('Данные в файле не являются списком: %s', file_path)
            return []

        # Нормализуем ключи, если это список словарей
        if data and isinstance(data[0], dict):
            return _normalize_dict_keys(data)
        return data

    except (json.JSONDecodeError, PermissionError, UnicodeDecodeError, OSError):
        logger.exception('Ошибка при чтении JSON‑файла %s', file_path)
        return []


def load_transactions_from_xlsx(file_name: str) -> list[dict[str, Any]]:
    """Загружает транзакции из XLSX‑файла (.xlsx, .xls) в папке DATA_DIR."""
    xlsx_path = DATA_DIR / file_name

    if not _validate_file(xlsx_path, ['.xlsx', '.xls']):
        return []

    try:
        logger.info('Читаем файл: %s', xlsx_path.name)
        xlsx_df = pd.read_excel(xlsx_path)
        logger.info('Успешно прочитано %s транзакций из %s', len(xlsx_df), xlsx_path.name)

        # Нормализуем ключи к str
        data = xlsx_df.to_dict('records')
        return _normalize_dict_keys(data)

    except pd.errors.EmptyDataError:
        logger.exception('Excel‑файл пуст: %s', xlsx_path.name)
        return []

    except ValueError:  # Например, неверный формат файла
        logger.exception('Ошибка чтения Excel‑файла %s', xlsx_path.name)
        return []

    except PermissionError:
        logger.exception('Нет доступа к файлу: %s', xlsx_path)
        return []

    except Exception:
        logger.exception('Неожиданная ошибка при чтении Excel: %s', xlsx_path.name)
        return []
