from collections.abc import Generator
from typing import Any


transactions = [
    {
        "id": 939719570,
        "state": "EXECUTED",
        "date": "2018-06-30T02:08:58.425572",
        "operationAmount": {"amount": "9824.07", "currency": {"name": "USD", "code": "USD"}},
        "description": "Перевод организации",
        "from": "Счет 75106830613657916952",
        "to": "Счет 11776614605963066702",
    },
    {
        "id": 142264268,
        "state": "EXECUTED",
        "date": "2019-04-04T23:20:05.206878",
        "operationAmount": {"amount": "79114.93", "currency": {"name": "USD", "code": "USD"}},
        "description": "Перевод со счета на счет",
        "from": "Счет 19708645243227258542",
        "to": "Счет 75651667383060284188",
    },
]


def filter_by_currency(
    transactions: list[dict[str, Any]], currency_code: str
) -> Generator[dict[str, Any], None, None]:
    """
    Фильтрует транзакции по коду валюты.

    Args:
        transactions: Список транзакций в виде словарей.
        currency_code: Код валюты (например, "USD").

    Yields:
        Транзакция, где валюта совпадает с currency_code.
    """
    for transaction in transactions:
        if (
            "operationAmount" in transaction
            and "currency" in transaction["operationAmount"]
            and "code" in transaction["operationAmount"]["currency"]
            and transaction["operationAmount"]["currency"]["code"] == currency_code
        ):
            yield transaction


usd_transactions = filter_by_currency(transactions, "USD")
for _ in range(2):
    print(next(usd_transactions))


def transaction_descriptions(
    transactions: list[dict[str, Any]], currency_code: str
) -> Generator[dict[str, Any], None, None]:
    for transaction in transactions:
        if (
            "operationAmount" in transaction
            and "currency" in transaction["operationAmount"]
            and "code" in transaction["operationAmount"]["currency"]
            and transaction["operationAmount"]["currency"]["code"] == currency_code
            and "description" in transaction  # проверяем наличие описания
        ):
            yield transaction["description"]  # правильный доступ к значению


# Получаем описания для USD
usd_descriptions = transaction_descriptions(transactions, "USD")

# Безопасный вывод (с обработкой StopIteration)
try:
    for _ in range(4):
        print(next(usd_descriptions))
except StopIteration:
    print("Больше нет описаний для USD")
