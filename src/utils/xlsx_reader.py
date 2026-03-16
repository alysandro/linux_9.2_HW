import atexit
import logging

import pandas as pd

from src.utils.constants import DATA_DIR
from src.utils.logging_config import setup_logger


# 1. Настраиваем именованный логгер для Excel
logger = setup_logger('xlsx_reader')

# Регистрируем корректное завершение
atexit.register(logging.shutdown)


def load_transactions_from_xlsx(file_name: str) -> list[dict]:
    """
    Загружает транзакции из любого xlsx_-файла (.xlsx, .xls) в папке DATA_DIR.
    """
    xlsx_path = DATA_DIR / file_name

    # 2. Проверка расширения (теперь для Excel)
    if xlsx_path.suffix.lower() not in ['.xlsx', '.xls']:
        logger.error(
            'Ошибка: Файл %s имеет неверное расширение. Ожидался .xlsx или .xls',
            xlsx_path.name,
        )
        return []

    # 3. Проверка существования файла
    if not xlsx_path.exists() or not xlsx_path.is_file():
        logger.error(
            'Файл не найден или не является файлом: %s',
            xlsx_path,
        )
        return []

    try:
        logger.info(
            'Читаем файл: %s',
            xlsx_path.name,
        )
        # Читаем Excel. Параметр engine='openpyxl' рекомендуется для .xlsx
        xlsx_df = pd.read_excel(xlsx_path)

        logger.info(
            'Успешно прочитано %s транзакций из %s',
            len(xlsx_df),
            xlsx_path.name,
        )

        # Возвращаем список словарей
        return xlsx_df.to_dict('records')

    except Exception:
        # Ловим только ошибки, связанные с файлами или неверным форматом Excel
        logger.exception(
            'Ошибка при чтении Excel файла: %s',
            xlsx_path.name,
        )
        return []


if __name__ == '__main__':
    # 1. Тестируем современный формат .xlsx
    xlsx_data = load_transactions_from_xlsx('transactions_excel.xlsx')
    if xlsx_data:
        # Используем f-строку для вывода первых двух записей
        print(f'Тестовый запуск XLSX: прочитано {len(xlsx_data)} строк. Примеры: {xlsx_data[:2]}')

    # 2. Тестируем старый формат .xls (если он есть в папке data)
    xls_data = load_transactions_from_xlsx('operations.xls')
    if xls_data:
        print(f'Тестовый запуск XLS: прочитано {len(xls_data)} строк. Примеры: {xls_data[:2]}')
