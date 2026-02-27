import json
from pathlib import Path
from typing import Any

from src.decorators.log_decorator import log
from src.utils.logging_config import logger


@log()
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
                logger.info(f'Успешно прочитано {len(result)} транзакций из {file_path}')
            else:
                logger.error('Данные в файле не являются списком: %s', file_path)

        except json.JSONDecodeError as e:
            logger.error('Ошибка парсинга JSON в файле %s: %s', file_path, e)
        except PermissionError:
            logger.error('Нет доступа к файлу: %s', file_path)
        except UnicodeDecodeError:
            logger.error('Неподдерживаемая кодировка в файле: %s', file_path)
        except OSError as e:
            logger.error('Ошибка ОС при чтении файла %s: %s', file_path, e)

    return result


if __name__ == '__main__':
    # Пример использования функции
    file_path = '/home/alexs/project/PyCharm/linux_9.2_HW/data/operations.json'
    transactions = read_transactions_from_json(file_path)
    print(transactions)
