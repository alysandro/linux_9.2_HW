from typing import Any

from src.external_api import convert_to_rub


def get_transaction_amount_in_rub(transaction: dict[str, Any]) -> float:
    """Принимает транзакцию и возвращает сумму в рублях (float)."""
    operation_amount = transaction.get('operationAmount', {})
    amount = operation_amount.get('amount')
    currency_info = operation_amount.get('currency', {})
    currency = currency_info.get('code')

    if amount is None or currency is None:
        return 0.0

    if currency == 'RUB':
        return float(amount)

    # Используем set literal (PLR6201)
    if currency in {'USD', 'EUR'}:
        return convert_to_rub(amount, currency)

    return float(amount)
