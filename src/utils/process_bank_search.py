import re


def process_bank_search(data: list[dict], search: str) -> list[dict]:
    """
    Ищет в описании операций заданную строку с использованием регулярных выражений.

    Args:
        data: список словарей с данными о банковских операциях
        search: строка поиска

    Returns:
        список словарей, у которых в описании есть данная строка
    """
    pattern = re.compile(re.escape(search), re.IGNORECASE)
    result = []

    for operation in data:
        description = operation.get('description', '')
        if pattern.search(description):
            result.append(operation)

    return result
