from __future__ import annotations


def mask_account_card(type_number: str) -> str:
    """
    Принимает номер счета или карты,
    по номеру определяет тип и выводить замаскированный номер счета или карты.
    """
    min_digits_line = 10
    line_card_min = 13
    line_card_max = 19
    # Удаляем все пробелы
    cleaned = ''.join(type_number.split())
    # Разделяем на слова и цифры
    cleaned_alpha = ''.join(filter(str.isalpha, cleaned))
    cleaned_digit = ''.join(filter(str.isdigit, cleaned))
    # Проверяем, что номер содержит хотя бы 10 цифр (минимум для маскировки)
    if len(cleaned_digit) < min_digits_line:
        raise ValueError('Номер должен содержать не менее 10 цифр')
    # Проверяем номер на соответствие Счет или Карта:
    if line_card_min <= len(cleaned_digit) <= line_card_max:
        first_6 = cleaned_digit[0:6]
        last_4 = cleaned_digit[-4:]
        # Формируем маскированный номер: XXXX XX** **** XXXX
        return f'{cleaned_alpha} {first_6[:4]} {first_6[4:6]}** **** {last_4}'

    last_4 = cleaned_digit[-4:]
    return f'{cleaned_alpha} ** {last_4}'


def get_date(date_string: str) -> str:
    """
    Фильтрует дату в формате # "ДД.ММ.ГГГГ"("11.03.2024")
    """
    # Разбиваем строку по символу 'T', берём первую часть — дату: "2024-03-11"
    date_part = date_string.split('T', maxsplit=1)[0]  # -> "2024-03-11"

    # Разбиваем по дефисам, получаем список: ['2024', '03', '11']
    parts = date_part.split('-')

    # Переставляем элементы в порядке ДД, ММ, ГГГГ через срезы (реверсивно, но с перестановкой) parts[2] — день,
    # parts[1] — месяц, parts[0] — год
    return f'"ДД.ММ.ГГГГ" - ("{parts[2]}.{parts[1]}.{parts[0]}")'
