from __future__ import annotations


def mask_account_card(type_number: str) -> str:
    '''
    Принимает номер счета или карты,
    по номеру определяет тип и выводить замаскированный номер счета или карты.
    '''
    # Удаляем все пробелы
    cleaned = ''.join(type_number.split())
    # Разделяем на слова и цифры
    cleaned_alpha = ''.join(filter(str.isalpha, cleaned))
    cleaned_digit = ''.join(filter(str.isdigit, cleaned))
    # Проверяем, что номер содержит хотя бы 10 цифр (минимум для маскировки)
    # if len(cleaned_digit) < 10:
    #     raise ValueError("Номер должен содержать не менее 10 цифр")
    # Проверяем номер на соответствие Счет или Карта:
    if 13 <= len(cleaned_digit) <= 19:
        first_6 = cleaned_digit[0:6]
        last_4 = cleaned_digit[-4:]
        # Формируем маскированный номер: XXXX XX** **** XXXX
        masked_card = f"{cleaned_alpha} {first_6[:4]} {first_6[4:6]}** **** {last_4}"
        return masked_card

    else:
        last_4 = cleaned_digit[-4:]
        masked_card = f"{cleaned_alpha} ** {last_4}"

    return masked_card


# Пример использования
type_number = 'Maestro 1596837868705199'
print(mask_account_card(type_number))

type_number = 'Счет 64686473678894779589'
print(mask_account_card(type_number))

type_number = 'MasterCard 7158300734726758'
print(mask_account_card(type_number))

type_number = 'Счет 35383033474447895560'
print(mask_account_card(type_number))

type_number = 'Visa Classic 6831982476737658'
print(mask_account_card(type_number))

type_number = 'Visa Platinum 8990922113665229'
print(mask_account_card(type_number))
''
type_number = 'Visa Gold 5999414228426353'
print(mask_account_card(type_number))

type_number = 'Счет 73654108430135874305'
print(mask_account_card(type_number))


def get_date(date_string: str) -> str:
    '''
    Фильтрует дату в формате # "ДД.ММ.ГГГГ"("11.03.2024")
    '''
    # Разбиваем строку по символу 'T', берём первую часть — дату: "2024-03-11"
    date_part = date_string.split('T')[0]  # -> "2024-03-11"

    # Разбиваем по дефисам, получаем список: ['2024', '03', '11']
    parts = date_part.split('-')

    # Переставляем элементы в порядке ДД, ММ, ГГГГ через срезы (реверсивно, но с перестановкой) parts[2] — день,
    # parts[1] — месяц, parts[0] — год
    formatted_date = f'"ДД.ММ.ГГГГ" - ("{parts[2]}.{parts[1]}.{parts[0]}")'

    return formatted_date


date_string = '2024-03-11T02:26:18.671407'
# и возвращает строку с датой в формате
print(get_date(date_string))
# "ДД.ММ.ГГГГ"("11.03.2024")
