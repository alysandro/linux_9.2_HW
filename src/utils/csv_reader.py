import atexit
import logging

import pandas as pd

from src.utils.constants import DATA_DIR
from src.utils.logging_config import setup_logger


# 1. Настраиваем именованный логгер
logger = setup_logger('csv_reader')

# Регистрируем корректное завершение (необязательно, но полезно для сложных систем)
atexit.register(logging.shutdown)


def load_transactions_from_csv(file_name: str) -> list[dict]:
    """
    Загружает транзакции из любого CSV-файла в папке DATA_DIR.
    Аргумент file_name позволяет обрабатывать разные файлы без правки кода.
    """
    csv_path = DATA_DIR / file_name

    # 2. Проверка расширения перед обработкой (как просили в задании)
    if csv_path.suffix.lower() != '.csv':
        logger.error(
            'Ошибка: Файл %s имеет неверное расширение. Ожидался .csv',
            csv_path.name,
        )
        return []

    # 3. Проверка существования файла перед чтением
    if not csv_path.exists() or not csv_path.is_file():
        logger.error('Файл не найден или не является файлом: %s', csv_path)
        return []

    try:
        logger.info('Читаем файл: %s', csv_path.name)
        csv_df = pd.read_csv(csv_path, sep=None, engine='python')
        logger.info('Успешно прочитано %s транзакций из %s', len(csv_df), csv_path.name)
        return csv_df.to_dict('records')  # Приводим к списку словарей для единообразия с JSON

    except Exception:
        # Ловим только ошибки, связанные с файлами или неверным форматом Excel
        logger.exception(
            'Ошибка при чтении CSV файла: %s',
            csv_path.name,
        )
        return []


if __name__ == '__main__':
    csv_data = load_transactions_from_csv('transactions.csv')
    if csv_data:
        print(f'Тестовый запуск CSV: Прочитано первые 2 записи: {csv_data[:2]}')
