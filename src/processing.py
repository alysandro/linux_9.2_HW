from __future__ import annotations

from typing import Any


def filter_by_state(
    data: list[dict[str, Any]],
    state: str = 'EXECUTED',
) -> list[dict[str, Any]]:
    """Функцию принимает список словарей и опционально
    значение для ключа state (по умолчанию 'EXECUTED')."""

    filtered_list = []
    for item in list_of_dicts:
        if item['state'] == state:
            filtered_list.append(item)
    return filtered_list  # Возвращаем список после завершения цикла


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
