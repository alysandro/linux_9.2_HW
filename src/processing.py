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
