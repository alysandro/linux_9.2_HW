from __future__ import annotations

from src.processing import filter_by_state


def test_filter_by_state():

    transactions = [
        {'id': 414288290, 'state': 'EXECUTED', 'date': '2019-07-03T18:35:29.512364'},
        {'id': 939719570, 'state': 'EXECUTED', 'date': '2018-06-30T02:08:58.425572'},
        {'id': 594226727, 'state': 'CANCELED', 'date': '2018-09-12T21:27:25.241689'},
        {'id': 615064591, 'state': 'CANCELED', 'date': '2018-10-14T08:21:33.419441'},
    ]

    # Тест 1: фильтруем по 'EXECUTED'
    assert filter_by_state(transactions, 'EXECUTED') == [
        {'id': 414288290, 'state': 'EXECUTED', 'date': '2019-07-03T18:35:29.512364'},
        {'id': 939719570, 'state': 'EXECUTED', 'date': '2018-06-30T02:08:58.425572'},
    ]

    # Тест 2: фильтруем по 'CANCELED'
    assert filter_by_state(transactions, 'CANCELED') == [
        {'id': 594226727, 'state': 'CANCELED', 'date': '2018-09-12T21:27:25.241689'},
        {'id': 615064591, 'state': 'CANCELED', 'date': '2018-10-14T08:21:33.419441'},
    ]

    # Тест 3: фильтруем по несуществующему состоянию (должен вернуть пустой список)
    assert filter_by_state(transactions, 'PENDING') == []
