from collections.abc import Generator, Iterable
from typing import Any


transactions = [
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
]


def filter_by_currency(transactions: Iterable[Any], currency_code: str) -> Generator[dict[str, Any], None, None]:
    """
    Фильтрует транзакции по коду валюты.

    Args:
        transactions: Список транзакций в виде словарей.
        currency_code: Код валюты (например, "USD").

    Yields:
        Транзакция, где валюта совпадает с currency_code.

    Примечания:
        Транзакции с отсутствующими или некорректными полями пропускаются
        с выводом предупреждения.
    """

    for idx, transaction in enumerate(transactions):
        if not isinstance(transaction, dict):
            print(f'Предупреждение: Транзакция #{idx} не является словарём. Пропускаем.')
            continue

        op_amount = transaction.get('operationAmount')
        if not isinstance(op_amount, dict):
            print(f"Предупреждение: В транзакции #{idx} некорректный 'operationAmount'. Пропускаем.")
            continue

        currency = op_amount.get('currency')
        if not isinstance(currency, dict):
            print(f"Предупреждение: В транзакции #{idx} некорректная 'currency'. Пропускаем.")
            continue

        code = currency.get('code')
        if not isinstance(code, str):
            print(f"Предупреждение: В транзакции #{idx} некорректное поле 'code'. Пропускаем.")
            continue

        if code != currency_code:
            print(f'[ПРОПУСК #{idx}] Валюта {code} ≠ {currency_code}. Пропускаем.')
        else:
            yield transaction


usd_transactions = filter_by_currency(transactions, 'USD')
for _ in range(2):
    print(next(usd_transactions))


def transaction_descriptions(
    transactions: list[dict[str, Any]], currency_code: str
) -> Generator[dict[str, Any], None, None]:
    for transaction in transactions:
        if (
            'operationAmount' in transaction
            and 'currency' in transaction['operationAmount']
            and 'code' in transaction['operationAmount']['currency']
            and transaction['operationAmount']['currency']['code'] == currency_code
            and 'description' in transaction  # проверяем наличие описания
        ):
            yield transaction['description']  # правильный доступ к значению


# Получаем описания для USD
usd_descriptions = transaction_descriptions(transactions, 'USD')

# Безопасный вывод (с обработкой StopIteration)
try:
    for _ in range(4):
        print(next(usd_descriptions))
except StopIteration:
    print('Больше нет описаний для USD')


def card_number_generator(start: int, end: int) -> Generator[str, None, None]:
    """
    Генератор номеров банковских карт в формате XXXX XXXX XXXX XXXX.

    Выдаёт номера карт в заданном диапазоне (включительно),
    дополняя их ведущими нулями до 16 цифр и разбивая на группы по 4.

    Args:
        start: Начальное число диапазона (от 1 до 9999999999999999).
        end: Конечное число диапазона (до 9999999999999999).

    Yields:
        Строка с номером карты в формате "XXXX XXXX XXXX XXXX".

    Raises:
        ValueError: Если start < 1, end > 9999999999999999 или start > end.

    Example:
        >>> for num in card_number_generator(1, 5):
        ...     print(num)
        0000 0000 0000 0001
        0000 0000 0000 0002
        0000 0000 0000 0003
        0000 0000 0000 0004
        0000 0000 0000 0005
    """
    start_card_number = 1
    end_card_number = 9999_9999_9999_9999
    # Проверка границ
    if start < start_card_number:
        raise ValueError('start должно быть ≥ 1')
    if end > end_card_number:
        raise ValueError('end не может превышать 9999999999999999')
    if start > end:
        raise ValueError('start не может быть больше end')

    for number in range(start, end + 1):
        # Форматируем число как 16‑значную строку с ведущими нулями
        card_str = f'{number:016d}'
        # Разбиваем на группы по 4 цифры
        yield f'{card_str[:4]} {card_str[4:8]} {card_str[8:12]} {card_str[12:16]}'
