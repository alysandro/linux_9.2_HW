from __future__ import annotations

import pytest

from src.masks import get_mask_account, get_mask_card_number


# Тестируем корректные данные
@pytest.mark.parametrize(
    ('value', 'expected'),
    [
        ('1234 1234 1234 1234', '1234 12** **** 1234'),
        ('1235 45584 54555', '1235 45** **** 4555'),
    ],
)
def test_get_mask_card_number(value, expected):
    assert get_mask_card_number(value) == expected


def test_invalid_card_number():
    """Тестируем некорректный ввод: проверяем ValueError и сообщения."""
    # Тест 1: слишком короткий номер (4 цифры)
    with pytest.raises(ValueError, match='Номер карты должен содержать не менее 10 цифр'):
        get_mask_card_number('1234')

    # Тест 2: 8 цифр (меньше 10)
    with pytest.raises(ValueError, match='Номер карты должен содержать не менее 10 цифр'):
        get_mask_card_number('12345678')

    # Тест 3: пустая строка
    with pytest.raises(ValueError, match='Номер карты не содержит цифр'):
        get_mask_card_number('')


def test_get_mask_account(mask_account):
    assert get_mask_account('15326548995852688589569') == mask_account
