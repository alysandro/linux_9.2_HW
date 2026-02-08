import copy

import pytest

from src.decorators.log_decorator import LOGS_DIR


@pytest.fixture
def mask_account():
    return '** 9569'


@pytest.fixture
def transactions():
    """Фикстура с тестовыми транзакциями."""
    return [
        {'id': 414288290, 'state': 'EXECUTED', 'date': '2019-07-03T18:35:29.512364'},
        {'id': 939719570, 'state': 'EXECUTED', 'date': '2018-06-30T02:08:58.425572'},
        {'id': 594226727, 'state': 'CANCELED', 'date': '2018-09-12T21:27:25.241689'},
        {'id': 615064591, 'state': 'CANCELED', 'date': '2018-10-14T08:21:33.419441'},
    ]


@pytest.fixture
def transactions_with_empty_code():
    return [
        {'id': 1242264268, 'operationAmount': {'currency': {'code': ''}}},
        {'id': 1242264278, 'operationAmount': {'currency': {'code': ''}}},
    ]


@pytest.fixture
def transaction_to_list():
    """Фикстура с тестовыми транзакциями."""
    return [
        {
            'id': 939719570,
            'state': 'EXECUTED',
            'date': '2018-06-30T02:08:58.425572',
            'operationAmount': {'amount': '9824.07', 'currency': {'name': 'USD', 'code': 'USD'}},
            'description': 'Перевод организации',
            'from': 'Счет 75106830613657916952',
            'to': 'Счет 11776614605963066702',
        },
        {
            'id': 142264268,
            'state': 'EXECUTED',
            'date': '2019-04-04T23:20:05.206878',
            'operationAmount': {'amount': '79114.93', 'currency': {'name': 'USD', 'code': 'USD'}},
            'description': 'Перевод со счета на счет',
            'from': 'Счет 19708645243227258542',
            'to': 'Счет 75651667383060284188',
        },
        {
            'id': 1239719570,
            'state': 'EXECUTED',
            'date': '2018-06-30T02:08:58.425572',
            'operationAmount': {'amount': '9824.07', 'currency': {'name': 'USD', 'code': 'USD'}},
            'description': 'Перевод организации',
            'from': 'Счет 75106830613657916952',
            'to': 'Счет 11776614605963066702',
        },
        {
            'id': 1242264268,
            'state': 'EXECUTED',
            'date': '2019-04-04T23:20:05.206878',
            'operationAmount': {'amount': '79114.93', 'currency': {'name': 'USD', 'code': 'USD'}},
            'description': 'Перевод со счета на счет',
            'from': 'Счет 19708645243227258542',
            'to': 'Счет 75651667383060284188',
        },
        {
            'id': 1239719570,
            'state': 'EXECUTED',
            'date': '2018-06-30T02:08:58.425572',
            'operationAmount': {'amount': '9824.07', 'currency': {'name': 'EUR', 'code': 'EUR'}},
            'description': 'Перевод организации',
            'from': 'Счет 75106830613657916952',
            'to': 'Счет 11776614605963066702',
        },
        {
            'id': 1242264268,
            'state': 'EXECUTED',
            'date': '2019-04-04T23:20:05.206878',
            'operationAmount': {'amount': '79114.93', 'currency': {'name': '', 'code': ''}},
            'description': 'Перевод со счета на счет',
            'from': 'Счет 19708645243227258542',
            'to': 'Счет 75651667383060284188',
        },
        {
            'id': 1242264278,
            'state': 'EXECUTED',
            'date': '2019-04-04T23:20:05.206878',
            'operationAmount': {'amount': '79114.93', 'currency': {'name': '', 'code': ''}},
            'description': 'Перевод со счета на счет',
            'from': 'Счет 19708645243227258542',
            'to': 'Счет 75651667383060284188',
        },
    ]


@pytest.fixture
def transaction_without_currency_code(transaction_to_list):
    transaction = copy.deepcopy(transaction_to_list)
    transaction[0]['operationAmount']['currency'].pop('code')
    return transaction


@pytest.fixture
def eur_transaction():
    return {'id': 1239719570, 'operationAmount': {'currency': {'code': 'EUR'}}}


@pytest.fixture
def log_file():
    LOGS_DIR.mkdir(exist_ok=True)
    print(f'Создана папка: {LOGS_DIR}')  # отладочный вывод
    path = LOGS_DIR / 'test_log.txt'
    if path.exists():
        path.unlink()
    print(f'Путь к файлу: {path}')  # отладочный вывод
    yield path
    if path.exists():
        path.unlink()
