import json
from pathlib import Path
from typing import Any

from src.utils.logging_config import get_module_logger


logger = get_module_logger('json_reader')


# @log()
def read_transactions_from_json(file_path: str) -> list[dict[str, Any]]:
    """
    Читает JSON‑файл с транзакциями и возвращает список словарей.

    Args:
        file_path (str): Путь к JSON‑файлу.

    Returns:
        list[dict[str, Any]]: Список транзакций или пустой список при ошибке.
    """
    path = Path(file_path)
    result: list[dict[str, Any]] = []

    # Объединённая проверка существования и типа файла
    if not path.exists() or not path.is_file():
        logger.error('Файл не найден или не является файлом: %s', file_path)
    else:
        try:
            with path.open('r', encoding='utf-8') as file:
                data = json.load(file)

            # Проверка типа данных
            if isinstance(data, list):
                result = data
                # ИСПРАВЛЕНО (G004): убрали f-строку, заменили на %s
                logger.info('Успешно прочитано %s транзакций из %s', len(result), path.name)
            else:
                logger.error('Данные в файле не являются списком: %s', file_path)

        except json.JSONDecodeError:
            # ИСПРАВЛЕНО (TRY400): заменили error на exception
            logger.exception('Ошибка парсинга JSON в файле %s', file_path)
        except PermissionError:
            logger.exception('Нет доступа к файлу: %s', file_path)
        except UnicodeDecodeError:
            logger.exception('Неподдерживаемая кодировка в файле: %s', file_path)
        except OSError:
            logger.exception('Ошибка ОС при чтении файла %s', file_path)

    return result
