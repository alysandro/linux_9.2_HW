from __future__ import annotations

import pytest

from src.masks import get_mask_account, get_mask_card_number


# Тестируем корректные данные
@pytest.mark.parametrize(
    "value, expected",
    [
        ("1234 1234 1234 1234", "1234 12** **** 1234"),
        ("1235 45584 54555", "1235 45** **** 4555"),
    ],
)
def test_get_mask_card_number(value, expected):
    assert get_mask_card_number(value) == expected


# def test_get_mask_card_number():
#     assert get_mask_card_number('1234 1234 1234 1234') == '1234 12** **** 1234'
#     assert get_mask_card_number('1235 45584 54555') == '1235 45** **** 4555'


def test_invalid_card_number():
    """Тестируем некорректный ввод: проверяем ValueError и сообщения."""
    # Тест 1: слишком короткий номер
    with pytest.raises(ValueError) as exc_info:
        get_mask_card_number("1234")
    assert str(exc_info.value) == "Номер карты должен содержать не менее 10 цифр"

    # Тест 2: 8 цифр (меньше 10)
    with pytest.raises(ValueError) as exc_info:
        get_mask_card_number("12345678")
    assert str(exc_info.value) == "Номер карты должен содержать не менее 10 цифр"

    # Тест 3: пустая строка
    with pytest.raises(ValueError) as exc_info:
        get_mask_card_number("")
    assert str(exc_info.value) == "Номер карты не содержит цифр"


def test_get_mask_account():
    assert get_mask_account("15326548995852688589569") == "** 9569"
