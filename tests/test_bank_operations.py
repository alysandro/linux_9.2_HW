import pytest

from src.processing.bank_operations import process_bank_operations, process_bank_search


@pytest.fixture
def sample_data():
    """Фикстура с тестовыми данными."""
    return [
        {
            'description': 'Перевод зарплаты',
            'status': 'EXECUTED',
            'date': '08.12.2019',
            'amount': '40542 руб.',
            'account': '**4321',
        },
        {
            'description': 'Оплата ЖКХ',
            'status': 'CANCELED',
            'date': '12.11.2019',
            'amount': '130 USD',
            'account': '7771 27** **** 3727',
        },
        {
            'description': 'Покупка продуктов',
            'status': 'EXECUTED',
            'date': '18.07.2018',
            'amount': '8390 руб.',
            'account': '**0034',
        },
        {
            'description': 'Перевод другу',
            'status': 'PENDING',
            'date': '03.06.2018',
            'amount': '8200 EUR',
            'account': '**2935',
        },
    ]


@pytest.fixture
def categories():
    """Фикстура с категориями для тестирования."""
    return ['Перевод', 'Оплата', 'Покупка']


# Тесты для process_bank_search
def test_process_bank_search_found(sample_data):
    result = process_bank_search(sample_data, 'Перевод')
    assert len(result) == 2
    assert any('Перевод зарплаты' in op['description'] for op in result)


def test_process_bank_search_not_found(sample_data):
    result = process_bank_search(sample_data, 'Неизвестная операция')
    assert len(result) == 0


def test_process_bank_search_case_insensitive(sample_data):
    result = process_bank_search(sample_data, 'перевод')
    assert len(result) == 2


def test_process_bank_search_empty_string(sample_data):
    result = process_bank_search(sample_data, '')
    assert result == sample_data


def test_process_bank_search_special_chars(sample_data):
    result = process_bank_search(sample_data, 'зарплаты')
    assert len(result) == 1
    assert 'Перевод зарплаты' in result[0]['description']


# Тесты для process_bank_operations
def test_process_bank_operations_counts(sample_data, categories):
    result = process_bank_operations(sample_data, categories)
    assert isinstance(result, dict)
    assert set(result.keys()) == set(categories)
    assert result['Перевод'] == 2
    assert result['Оплата'] == 1
    assert result['Покупка'] == 1


def test_process_bank_operations_empty_data():
    empty_data = []
    categories = ['Перевод', 'Оплата']
    result = process_bank_operations(empty_data, categories)
    assert result == {'Перевод': 0, 'Оплата': 0}


def test_process_bank_operations_no_matching_categories(sample_data):
    categories = ['Инвестиции', 'Страхование']
    result = process_bank_operations(sample_data, categories)
    assert result == {'Инвестиции': 0, 'Страхование': 0}


def test_process_bank_operations_partial_match(sample_data):
    categories = ['Пере', 'Опл']
    result = process_bank_operations(sample_data, categories)
    assert result['Пере'] == 2
    assert result['Опл'] == 1
