def process_bank_operations(data: list[dict], categories: list) -> dict:
    """
    Подсчитывает количество операций в каждой категории.

    Args:
        data: список словарей с данными о банковских операциях
        categories: список категорий операций

    Returns:
        словарь с количеством операций в каждой категории
    """
    result = dict.fromkeys(categories, 0)

    for operation in data:
        description = operation.get('description', '').lower()
        for category in categories:
            if category.lower() in description:
                result[category] += 1

    return result
