from __future__ import annotations

from datetime import datetime
from typing import Any


def filter_by_state(
    data: list[dict[str, Any]],
    state: str = 'EXECUTED',
) -> list[dict[str, Any]]:
    """Функция принимает список словарей и опционально
    значение для ключа state (по умолчанию 'EXECUTED').

    Возвращает новый список словарей, у которых 'state' совпадает с указанным.
    """
    return [item for item in data if item['state'] == state]


def sort_by_date(
    list_of_dicts: list[dict[str, Any]],
    *,
    reverse: bool = True,
) -> list[dict[str, Any]]:
    """
    Сортирует список словарей по дате в поле 'date'.

    Args:
        list_of_dicts: Список словарей с ключом 'date' в формате ISO 8601.
        reverse: Порядок сортировки. True — по убыванию, False — по возрастанию.
        По умолчанию True.

    Returns:
        Новый отсортированный список словарей.
    """
    return sorted(
        list_of_dicts,
        key=lambda x: datetime.fromisoformat(x['date']),
        reverse=reverse,
    )


# Пример данных
list_of_dicts = [
    {'id': 414288290, 'state': 'EXECUTED', 'date': '2019-07-03T18:35:29.512364'},
    {'id': 939719570, 'state': 'EXECUTED', 'date': '2018-06-30T02:08:58.425572'},
    {'id': 594226727, 'state': 'CANCELED', 'date': '2018-09-12T21:27:25.241689'},
    {'id': 615064591, 'state': 'CANCELED', 'date': '2018-10-14T08:21:33.419441'},
]


# Примеры использования
executed_transactions = filter_by_state(list_of_dicts, 'EXECUTED')
print('Выполненные операции:')
print(executed_transactions)

canceled_transactions = filter_by_state(list_of_dicts, 'CANCELED')
print('\nОтменённые операции:')
print(canceled_transactions)

sorted_transactions = sort_by_date(list_of_dicts)
print('\nОперации по дате (по убыванию):')
print(sorted_transactions)
