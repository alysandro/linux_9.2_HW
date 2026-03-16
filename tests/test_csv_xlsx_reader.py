from unittest.mock import patch

import pandas as pd
import pytest

from src.utils.csv_reader import load_transactions_from_csv
from src.utils.xlsx_reader import load_transactions_from_xlsx


# Фикстура для создания временного CSV
@pytest.fixture
def temp_csv(tmp_path):
    file_path = tmp_path / 'test.csv'
    df = pd.DataFrame([{'id': 1, 'amount': 100}, {'id': 2, 'amount': 200}])
    df.to_csv(file_path, index=False)
    return file_path


# Фикстура для создания временного XLSX
@pytest.fixture
def temp_xlsx(tmp_path):
    file_path = tmp_path / 'test.xlsx'
    df = pd.DataFrame([{'id': 3, 'amount': 300}])
    df.to_excel(file_path, index=False)
    return file_path


def test_load_csv_success(temp_csv):
    expected_count = 2
    expected_amount = 100
    # Патчим DATA_DIR, чтобы функция искала файл в нашей временной папке
    with patch('src.utils.csv_reader.DATA_DIR', temp_csv.parent):
        result = load_transactions_from_csv('test.csv')
        assert len(result) == expected_count
        assert result[0]['amount'] == expected_amount


def test_load_xlsx_success(temp_xlsx):
    expected_count = 1
    expected_amount = 300
    with patch('src.utils.xlsx_reader.DATA_DIR', temp_xlsx.parent):
        result = load_transactions_from_xlsx('test.xlsx')
        assert len(result) == expected_count
        assert result[0]['amount'] == expected_amount


def test_load_csv_file_not_found():
    result = load_transactions_from_csv('non_existent.csv')
    assert result == []


def test_load_xlsx_invalid_extension():
    # Проверка, что на неправильное расширение вернется пустой список
    result = load_transactions_from_xlsx('test.txt')
    assert result == []


# 1. Тест на ошибку расширения (для CSV)
def test_load_csv_invalid_extension():
    result = load_transactions_from_csv('test.txt')  # Подсовываем .txt
    assert result == []


# 2. Тест на несуществующий файл (для XLSX)
def test_load_xlsx_file_not_found():
    result = load_transactions_from_xlsx('ghost.xlsx')
    assert result == []


# 3. Тест на критическую ошибку (симуляция битого файла)
def test_load_csv_critical_error():
    with patch('pandas.read_csv') as mock_read:
        mock_read.side_effect = Exception('Boom!')  # Симулируем взрыв при чтении
        result = load_transactions_from_csv('transactions.csv')
        assert result == []
