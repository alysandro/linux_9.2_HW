from __future__ import annotations

from src.generators import filter_by_currency


def test_filter_by_currency_usd(transaction_to_list):
    """Тест: фильтрация по USD."""
    usd_tran_count = 4  # Ожидаемое количество транзакций в USD
    usd_tran_id = 939719570  # ID первой транзакции в USD
    result = list(filter_by_currency(transaction_to_list, 'USD'))
    assert len(result) == usd_tran_count
    assert result[0]['id'] == usd_tran_id
    assert result[0]['operationAmount']['currency']['code'] == 'USD'


def test_filter_by_currency_with_eur(eur_transaction):
    """Тест: фильтрация по EUR."""
    transaction_list = [eur_transaction]  # Или добавьте в общий список транзакций
    result = list(filter_by_currency(transaction_list, 'EUR'))

    assert result[0]['id'] == eur_transaction['id']
    assert result[0]['operationAmount']['currency']['code'] == 'EUR'
    assert len(result) == 1


def test_filter_by_currency_empty_list():
    """Тест: пустой список транзакций."""
    result = list(filter_by_currency([], 'USD'))
    assert len(result) == 0


def test_filter_by_currency_invalid(transactions_with_empty_code):
    result = list(filter_by_currency(transactions_with_empty_code, ''))

    # Ожидаем столько транзакций, сколько передано в фикстуре
    assert len(result) == len(transactions_with_empty_code)
    assert not result[0]['operationAmount']['currency']['code']
