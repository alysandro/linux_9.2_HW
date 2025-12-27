from __future__ import annotations

from src.masks import get_mask_account
from src.masks import get_mask_card_number


def test_get_mask_card_number():
    assert get_mask_card_number('1234 1234 1234 1234') == '1234 12** **** 1234'
    assert get_mask_card_number('1235 45584 54555') == '1235 45** **** 4555'


def test_get_mask_account():
    assert get_mask_account('15326548995852688589569') == '** 9569'
