from __future__ import annotations

import pytest

from src.masks import get_mask_account
from src.masks import get_mask_card_number


# Тестируем корректные данные
def test_get_mask_card_number():
    assert get_mask_card_number('1234 1234 1234 1234') == '1234 12** **** 1234'
    assert get_mask_card_number('1235 45584 54555') == '1235 45** **** 4555'

    # Тестируем некорректный ввод: проверяем,
    # что выбрасывается ValueError с правильным сообщением
    with pytest.raises(ValueError) as exc_info:
        get_mask_card_number('12345678')  # меньше 10 цифр

    assert str(exc_info.value) == 'Номер карты должен содержать не менее 10 цифр'

    # Дополнительно: тест на пустой ввод
    with pytest.raises(ValueError) as exc_info:
        get_mask_card_number('')
    assert str(exc_info.value) == 'Номер карты не содержит цифр'


def test_get_mask_account():
    assert get_mask_account('15326548995852688589569') == '** 9569'
