import logging

import pytest

from src.new_generators import filter_by_currency


# Отключаем логирование для тестов
logging.disable(logging.WARNING)


@pytest.fixture
def sample_transactions():
    return [
        {'amount': 100, 'currency_code': 'RUB'},
        {'amount': 200, 'currency_details': {'code': 'USD'}},
        {'amount': 300, 'currency': 'руб.'},
        {'amount': 400, 'unrelated': 'EUR'},
        {'amount': 500},  # без валюты
    ]


class TestFilterByCurrency:
    def test_filter_rub_variations(self, sample_transactions):
        result = list(filter_by_currency(sample_transactions, 'RUB'))
        assert len(result) == 2
        assert result[0]['amount'] == 100
        assert result[1]['amount'] == 300

    def test_filter_usd(self, sample_transactions):
        result = list(filter_by_currency(sample_transactions, 'USD'))
        assert len(result) == 1
        assert result[0]['amount'] == 200

    def test_no_matching_currency(self, sample_transactions):
        result = list(filter_by_currency(sample_transactions, 'EUR'))
        assert len(result) == 0

    def test_empty_transactions(self):
        result = list(filter_by_currency([], 'RUB'))
        assert len(result) == 0
