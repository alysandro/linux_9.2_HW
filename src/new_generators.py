from collections.abc import Generator, Iterable
import re


def filter_by_currency(transactions: Iterable[dict], currency_code: str) -> Generator[dict, None, None]:
    """
    Универсальный генератор.
    Ищет валюту в JSON, CSV и Excel одинаково успешно.

    Args:
        transactions: Итерируемый объект с транзакциями (список словарей).
        currency_code: Код валюты для фильтрации (например, 'RUB', 'USD').

    Yields:
        Словари транзакций, где найдена указанная валюта.
    """
    target = currency_code.upper()
    is_rub = target == 'RUB'

    # Нормализованные варианты для RUB
    rub_variants = {'РУБ', 'РУБЛИ', 'РУБЛЬ', 'RUB', 'РУБ.'}

    for tx in transactions:
        found_match = False

        for k, v in tx.items():
            # Проверяем ключевые поля, связанные с валютой
            if re.search(r'currency', k, re.IGNORECASE):
                if isinstance(v, dict):
                    # Обрабатываем вложенные структуры (JSON)
                    for nested_key, nested_val in v.items():
                        if nested_key.lower() == 'code':
                            val_upper = str(nested_val).upper()
                            if val_upper == target:
                                found_match = True
                                break
                else:
                    val_upper = str(v).upper()
                    if val_upper == target or (is_rub and val_upper in rub_variants):
                        found_match = True
                        break

        if found_match:
            yield tx
