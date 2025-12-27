from __future__ import annotations

from src.widget import get_date
from src.widget import mask_account_card


def test_mask_account_card():
    assert mask_account_card('Maestro 1596837868705199') == ('Maestro 1596 83** **** 5199')
    assert mask_account_card('Счет 64686473678894779589') == ('Счет ** 9589')
    assert mask_account_card('MasterCard 7158300734726758') == ('MasterCard 7158 30** **** 6758')
    assert mask_account_card('Счет 35383033474447895560') == ('Счет ** 5560')
    assert mask_account_card('Visa Classic 6831982476737658') == ('VisaClassic 6831 98** **** 7658')
    assert mask_account_card('Visa Platinum 8990922113665229') == ('VisaPlatinum 8990 92** **** 5229')
    assert mask_account_card('Visa Gold 5999414228426353') == ('VisaGold 5999 41** **** 6353')
    assert mask_account_card('Счет 73654108430135874305') == ('Счет ** 4305')


def test_get_date():
    assert get_date('2024-03-11T02:26:18.671407') == ('"ДД.ММ.ГГГГ" - ("11.03.2024")')
