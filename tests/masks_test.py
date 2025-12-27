from __future__ import annotations

from src.masks import get_mask_card_number


assert get_mask_card_number('1234 1234 1234 1234') == '1234 12** **** 1234'

# Формируем маскированный номер: XXXX XX** **** XXXX
# masked = f"{first_6[:4]} {first_6[4:6]}** **** {last_4}"
#
# return masked


# # Пример использования
# card = '4532 1234 5678 9012'
# print(get_mask_card_number(card))
#
#
# #     Функцию маскировки номера банковского счета
# def get_mask_account(acc_number: str) -> str:
#     '''Функцию маскировки номера банковского счета. Выводит последние цыфры счета'''
#     mask_account = f"{'**'} {acc_number[-4:]}"
#     return mask_account
#
#
# acc_number = '15326548995852688589569'
# print(get_mask_account(acc_number))
