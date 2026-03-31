import re


def process_bank_search(data: list[dict], search: str) -> list[dict]:
    """
    Ищет операции, в описании которых есть заданная строка (без учёта регистра).

    Args:
        data: список словарей с данными о банковских операциях
        search: строка для поиска

    Returns:
        Список словарей, содержащих искомую строку в описании
    """
    pattern = re.compile(re.escape(search), re.IGNORECASE)
    result = []

    for operation in data:
        description = operation.get('description', '')
        if pattern.search(description):
            result.append(operation)

    return result


def process_bank_operations(data: list[dict], categories: list[str]) -> dict[str, int]:
    """
    Подсчитывает количество операций в каждой категории.

    Args:
        data: список словарей с данными о банковских операциях
        categories: список категорий для подсчёта

    Returns:
        Словарь с количеством операций по каждой категории
    """
    category_counts = dict.fromkeys(categories, 0)

    for operation in data:
        description = operation.get('description', '').lower()
        for category in categories:
            if category.lower() in description:
                category_counts[category] += 1

    return category_counts
