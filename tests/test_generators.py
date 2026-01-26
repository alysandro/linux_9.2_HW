from __future__ import annotations

import pytest

from src.generators import card_number_generator, filter_by_currency, transaction_descriptions


def test_filter_by_currency_full_coverage():
    """Тест всех сценариев фильтрации для 100% покрытия."""
    mixed_data = [
        # 0. Успешный случай
        {'operationAmount': {'currency': {'code': 'USD'}}, 'id': 1},
        # 1. Не словарь
        'not a dict',
        # 2. Нет operationAmount
        {'id': 2},
        # 3. operationAmount не словарь
        {'operationAmount': 'not_dict', 'id': 3},
        # 4. Нет currency
        {'operationAmount': {}, 'id': 4},
        # 5. currency не словарь
        {'operationAmount': {'currency': 'not_dict'}, 'id': 5},
        # 6. Нет code
        {'operationAmount': {'currency': {}}, 'id': 6},
        # 7. Другая валюта
        {'operationAmount': {'currency': {'code': 'EUR'}}, 'id': 7},
    ]

    # Запускаем фильтрацию по USD
    result = list(filter_by_currency(mixed_data, 'USD'))

    # Должна остаться только первая транзакция
    assert len(result) == 1
    assert result[0]['id'] == 1
    assert result[0]['operationAmount']['currency']['code'] == 'USD'


def test_filter_by_currency_empty():
    """Тест с пустым списком."""
    assert list(filter_by_currency([], 'USD')) == []


def test_filter_by_currency_all_branches(transaction_to_list):
    """Тест для покрытия всех веток генератора фильтрации."""
    # Тестируем случай, когда валюта не совпадает
    result = list(filter_by_currency(transaction_to_list, 'GBP'))
    assert len(result) == 0


""" 96->95, 110->117, 145, 147, 149"""


def test_card_number_generator():
    """Тестируем генератор номеров карт"""
    generator = card_number_generator(1, 3)
    assert next(generator) == '0000 0000 0000 0001'
    assert next(generator) == '0000 0000 0000 0002'
    assert next(generator) == '0000 0000 0000 0003'


def test_card_number_generator_exceptions():
    """Тестируем валидацию границ (ValueError)."""

    # 1. Проверка start < 1
    with pytest.raises(ValueError, match='start должно быть ≥ 1'):
        next(card_number_generator(0, 10))

    # 2. Проверка start > end
    with pytest.raises(ValueError, match='start не может быть больше end'):
        next(card_number_generator(50, 10))

    # 3. Проверка end > 9999_9999_9999_9999
    with pytest.raises(ValueError, match='end не может превышать 9999999999999999'):
        next(card_number_generator(1, 10**16))


def test_transaction_descriptions(transaction_to_list):
    """Тестируем получение описаний из списка транзакций."""
    # Передаем список транзакций (фикстуру) напрямую
    descriptions = transaction_descriptions(transaction_to_list, 'USD')

    # Проверяем описания согласно вашей фикстуре в conftest.py
    # 1-я транзакция: 'Перевод организации'
    assert next(descriptions) == 'Перевод организации'
    # 2-я транзакция: 'Перевод со счета на счет'
    assert next(descriptions) == 'Перевод со счета на счет'
    # 3-я транзакция: 'Перевод организации'
    assert next(descriptions) == 'Перевод организации'
