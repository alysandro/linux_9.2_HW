import math
from unittest.mock import patch

from src.external_api.currency_converter import convert_to_rub
from src.utils.logging_config import setup_logger


setup_logger('old_mod', mode='a')


EXPECTED_USD_RATE = 90.0
EXPECTED_EUR_RATE = 100.0


@patch('src.external_api.currency_converter.get_exchange_rate')
def test_convert_to_rub_usd(mock_get_rate):
    mock_get_rate.return_value = EXPECTED_USD_RATE
    transaction = {'amount': 2, 'currency': 'USD', 'transaction_id': 'tx_1'}
    result = convert_to_rub(**transaction)
    assert result == 2 * EXPECTED_USD_RATE


@patch('src.external_api.currency_converter.get_exchange_rate')
def test_convert_to_rub_eur(mock_get_rate):
    mock_get_rate.return_value = EXPECTED_EUR_RATE
    transaction = {'amount': 1.5, 'currency': 'EUR', 'transaction_id': 'tx_2'}
    result = convert_to_rub(**transaction)
    assert math.isclose(result, 1.5 * EXPECTED_EUR_RATE, abs_tol=1e-9)


def test_convert_to_rub_rub():
    transaction = {'amount': 500, 'currency': 'RUB', 'transaction_id': 'tx_3'}
    result = convert_to_rub(**transaction)
    expected_amount = 500.0
    assert result == expected_amount


def test_convert_to_rub_invalid_amount():
    result = convert_to_rub('abc', 'USD', 'tx_4')
    assert math.isclose(result, 0.0, abs_tol=1e-9)
