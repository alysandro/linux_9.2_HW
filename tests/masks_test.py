import pytest

from src.masks import apply_masks, get_mask_account, get_mask_card_number


class TestMasks:
    @pytest.mark.parametrize(
        ('value', 'expected'),
        [
            ('1234 1234 1234 1234', '1234 12** **** 1234'),
            ('1235 45584 54555', '1235 45** **** 4555'),
        ],
    )
    def test_get_mask_card_number(self, value, expected):
        assert get_mask_card_number(value) == expected

    def test_invalid_card_number_short(self):
        with pytest.raises(ValueError, match='Номер карты должен содержать не менее 10 цифр'):
            get_mask_card_number('1234')

    def test_invalid_card_number_no_digits(self):
        with pytest.raises(ValueError, match='Номер карты не содержит цифр'):
            get_mask_card_number('')

    @pytest.fixture
    def mask_account(self):
        return '** 9569'

    def test_get_mask_account_valid(self, mask_account):
        result = get_mask_account('15326548995852688589569')
        assert result == mask_account

    def test_get_mask_account_short(self):
        result = get_mask_account('123')
        assert result == 'Invalid account number'


def test_get_mask_card_number_empty():
    with pytest.raises(ValueError, match='Номер карты не содержит цифр'):
        get_mask_card_number('')


def test_get_mask_account_exactly_4_digits():
    result = get_mask_account('1234')
    assert result == '** 1234'


def test_get_mask_account_less_than_4_digits():
    result = get_mask_account('123')
    assert result == 'Invalid account number'


def test_get_mask_card_number_with_spaces_and_letters():
    result = get_mask_card_number('Visa 1234-5678-9012-3456')
    assert result == '1234 56** **** 3456'


def test_apply_masks():
    test_data = [
        {'account': '15326548995852688589569', 'card': '1234123412341234'},
        {'account': '321', 'card': '5555444433332222'},
    ]
    result = apply_masks(test_data)
    assert result[0]['account'] == '** 9569'
    assert result[0]['card'] == '1234 12** **** 1234'
    assert result[1]['account'] == 'Invalid account number'
    assert result[1]['card'] == '5555 44** **** 2222'
