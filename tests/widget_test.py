from __future__ import annotations

import pytest

from src.widget import get_date, mask_account_card


@pytest.mark.parametrize(
    ('type_number', 'expected'),
    [
        ('Maestro 1596837868705199', 'Maestro 1596 83** **** 5199'),
        ('Счет 64686473678894779589', 'Счет ** 9589'),
        ('MasterCard 7158300734726758', 'MasterCard 7158 30** **** 6758'),
        ('Счет 35383033474447895560', 'Счет ** 5560'),
        ('Visa Classic 6831982476737658', 'VisaClassic 6831 98** **** 7658'),
        ('Visa Platinum 8990922113665229', 'VisaPlatinum 8990 92** **** 5229'),
        ('Visa Gold 5999414228426353', 'VisaGold 5999 41** **** 6353'),
        ('Счет 73654108430135874305', 'Счет ** 4305'),
        ('Карта 15236', 'Номер должен содержать не менее 10 цифр'),
    ],
)
def test_mask_account_card(type_number, expected):
    """Тест функции mask_account_card с параметризацией."""
    if expected == 'Номер должен содержать не менее 10 цифр':
        with pytest.raises(ValueError, match=expected):
            mask_account_card(type_number)
    else:
        assert mask_account_card(type_number) == expected


def test_get_date():
    assert get_date('2024-03-11T02:26:18.671407') == ('"ДД.ММ.ГГГГ" - ("11.03.2024")')
