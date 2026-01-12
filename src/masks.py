# Реализуйте в этом модуле две функции:
#     Функцию маскировки номера банковской карты
from __future__ import annotations


def get_mask_card_number(card: str) -> str:
    '''Функцию маскировки номера банковской карты. Выводит в формате: XXXX XX** **** XXXX'''
    # Удаляем все пробелы и нецифровые символы
    cleaned = ''.join(filter(str.isdigit, card))
    if not cleaned:
        raise ValueError('Номер карты не содержит цифр')
    # Проверяем, что номер содержит хотя бы 10 цифр (минимум для маскировки)
    if len(cleaned) < 10:
        raise ValueError('Номер карты должен содержать не менее 10 цифр')

    first_6 = cleaned[0:6]
    last_4 = cleaned[-4:]
    # Формируем маскированный номер: XXXX XX** **** XXXX
    masked = f"{first_6[:4]} {first_6[4:6]}** **** {last_4}"

    return masked


# Пример использования
# card = '4532 1234 5678 9012'
# card1 = '1235 45584 54555'
# card3 = '12345678'
# card4 = ''
# print(get_mask_card_number(card))
# print(get_mask_card_number(card1))
# print(get_mask_card_number(card3))
# print(get_mask_card_number(card4))


#     Функцию маскировки номера банковского счета
def get_mask_account(acc_number: str) -> str:
    '''Функцию маскировки номера банковского счета. Выводит последние цыфры счета'''
    mask_account = f"{'**'} {acc_number[-4:]}"
    return mask_account


# acc_number = '15326548995852688589569'
# print(get_mask_account(acc_number))
