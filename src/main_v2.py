from datetime import UTC, datetime
from enum import Enum
from typing import Any

from src.processing.bank_operations import process_bank_search
from src.utils.file_loader import load_transactions_from_csv, load_transactions_from_xlsx, read_transactions_from_json
from src.utils.logging_config import LoggerConfig, setup_logger


# Создание конфигурации
config = LoggerConfig(name='my_app', level_file='DEBUG', level_console='INFO', log_format='color')


# Инициализация логгера
logger = setup_logger(config)


def parse_date(date_str: str) -> datetime | None:
    """Парсит дату из строки с указанием временной зоны."""
    if not date_str:
        return None
    try:
        return datetime.strptime(date_str, '%d.%m.%Y').replace(tzinfo=UTC)

    except (ValueError, TypeError):
        return None


def filter_by_status(
    data: list[dict[str, Any]], status: str, valid_statuses: list[str] | None = None
) -> list[dict[str, Any]]:
    """Фильтрует операции по статусу (без учёта регистра)."""
    if valid_statuses is None:
        valid_statuses = ['EXECUTED', 'CANCELED', 'PENDING']

    status_lower = status.lower()
    if status_lower not in [s.lower() for s in valid_statuses]:
        logger.error('Недопустимый статус: %s. Доступные: %s', status, ', '.join(valid_statuses))
        raise ValueError(f'Недопустимый статус: {status}. Доступные: {", ".join(valid_statuses)}')
    return [op for op in data if op.get('status', '').lower() == status_lower]


class SortOrder(Enum):
    ASCENDING = 'asc'
    DESCENDING = 'desc'


def get_sort_key(op: dict[str, Any]) -> datetime:
    date_str = op.get('date', '')
    parsed = parse_date(date_str)
    return parsed or datetime.min.replace(tzinfo=UTC)


def sort_by_date(data: list[dict[str, Any]], order: SortOrder = SortOrder.ASCENDING) -> list[dict[str, Any]]:
    """Сортирует операции по дате.

    Args:
        data: список операций с полем 'date'
        order: порядок сортировки (по возрастанию или убыванию)
    """
    reverse = order == SortOrder.DESCENDING
    return sorted(data, key=get_sort_key, reverse=reverse)


def filter_ruble_transactions(data: list[dict[str, Any]]) -> list[dict[str, Any]]:
    """Оставляет только рублёвые транзакции."""
    ruble_indicators = ['руб', 'rub', 'rur']
    result = []
    for op in data:
        amount_str = str(op.get('amount', '')).lower()
        if any(indicator in amount_str for indicator in ruble_indicators):
            result.append(op)
    return result


class OutputMode(Enum):
    WITH_TOTAL = 'with_total'
    WITHOUT_TOTAL = 'without_total'


def print_operations(operations: list[dict[str, Any]], mode: OutputMode = OutputMode.WITH_TOTAL) -> None:
    """Выводит операции в заданном формате.

    Args:
        operations: список операций для вывода
        mode: режим вывода (с общей суммой или без)
    """
    if not operations:
        print('Операций нет')
        return

    for op in operations:
        print(f'Операция: {op}')

    if mode == OutputMode.WITH_TOTAL:
        total = sum(op.get('amount', 0) for op in operations)
        print(f'Общая сумма: {total}')


def load_data_by_choice(choice: str) -> list[dict[str, Any]]:
    """Загружает данные в зависимости от выбора пользователя."""
    loaders = {
        '1': lambda: read_transactions_from_json('transactions.json'),
        '2': lambda: load_transactions_from_csv('transactions.csv'),
        '3': lambda: load_transactions_from_xlsx('transactions.xlsx'),
    }
    loader = loaders.get(choice)
    if loader:
        return loader()
    print('Программа: Неверный выбор файла.')
    return []


def get_user_choices() -> dict[str, str | bool | None]:
    """Получает все выборы пользователя."""
    choices: dict[str, str | bool | None] = {}

    # Выбор файла
    print('Выберите необходимый пункт меню:')
    print('1. Получить информацию о транзакциях из JSON‑файла')
    print('2. Получить информацию о транзакциях из CSV‑файла')
    print('3. Получить информацию о транзакциях из XLSX‑файла')
    choices['file'] = input('Пользователь: ')

    # Статус
    valid_statuses = ['EXECUTED', 'CANCELED', 'PENDING']
    while True:
        print('Введите статус для фильтрации:')
        print(f'Доступные: {", ".join(valid_statuses)}')
        status = input('Пользователь: ').strip()
        if status.upper() in valid_statuses:
            choices['status'] = status
            break
        print(f'Статус "{status}" недоступен.')

    # Сортировка
    choices['sort'] = input('Отсортировать по дате? Да/Нет\nПользователь: ').lower()
    if choices['sort'] in ['да', 'yes']:
        order = input('По возрастанию или убыванию?\nПользователь: ').lower()
        choices['ascending'] = order == 'возрастанию'

    # Рублёвые
    choices['ruble'] = input('Только рублёвые? Да/Нет\nПользователь: ').lower()

    # Поиск
    choices['search'] = input('Фильтровать по слову в описании? Да/Нет\nПользователь: ').lower()
    if choices['search'] in ['да', 'yes']:
        choices['search_term'] = input('Введите слово для поиска:\nПользователь: ')

    return choices


def apply_filters(data: list[dict[str, Any]], choices: dict[str, str | bool | None]) -> list[dict[str, Any]]:
    """Применяет все фильтры к данным."""
    filtered = data

    # По статусу
    status_str = str(choices['status'])
    filtered = filter_by_status(filtered, status_str)

    # Сортировка
    if choices.get('sort') in ['да', 'yes']:
        ascending = choices.get('ascending', True)
        ascending_bool = ascending.lower() in ['да', 'yes', 'true'] if isinstance(ascending, str) else bool(ascending)
        order = SortOrder.ASCENDING if ascending_bool else SortOrder.DESCENDING
        filtered = sort_by_date(filtered, order)

    # Рублёвые
    if choices.get('ruble') in ['да', 'yes']:
        filtered = filter_ruble_transactions(filtered)

    # Поиск (временно закомментировано до реализации process_bank_search)
    if choices.get('search') in ['да', 'yes']:
        search_term = str(choices.get('search_term', '')).strip()
        if search_term:  # проверяем, что строка не пустая после strip()
            search_term_str = str(search_term)
            filtered = process_bank_search(filtered, search_term_str)

    return filtered


def main() -> None:
    """Основная функция программы."""
    print('Программа: Привет! Добро пожаловать в программу работы с банковскими транзакциями.')

    # Получаем выбор пользователя
    choices = get_user_choices()

    # Загружаем данные
    file_choice_str = str(choices['file'])
    data = load_data_by_choice(file_choice_str)
    if not data:
        return

    # Применяем все фильтры и сразу выводим результат
    print('Программа: Распечатываю итоговый список транзакций...')
    print_operations(apply_filters(data, choices))


if __name__ == '__main__':
    main()
