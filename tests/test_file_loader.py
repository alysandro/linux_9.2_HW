import json
from unittest.mock import patch

import pandas as pd

from src.utils.file_loader import (
    _normalize_dict_keys,
    _validate_file,
    load_transactions_from_csv,
    load_transactions_from_xlsx,
    read_transactions_from_json,
)


def test_normalize_dict_keys_with_non_str_keys():
    data = [{1: 'a', 2: 'b'}]
    result = _normalize_dict_keys(data)
    assert result == [{'1': 'a', '2': 'b'}]


def test_load_xlsx_empty(tmp_path):
    xlsx_file = tmp_path / 'empty.xlsx'
    xlsx_file.write_text('')  # Битый или пустой файл
    with patch('src.utils.file_loader.DATA_DIR', tmp_path):
        assert load_transactions_from_xlsx('empty.xlsx') == []


def test_load_csv_permission_error(tmp_path):
    csv_file = tmp_path / 'locked.csv'
    csv_file.write_text('id,amount\n1,100')
    with patch('src.utils.file_loader.DATA_DIR', tmp_path), patch('pandas.read_csv', side_effect=PermissionError):
        assert load_transactions_from_csv('locked.csv') == []


def test_read_json_not_list(tmp_path):
    json_file = tmp_path / 'not_list.json'
    json_file.write_text(json.dumps({'a': 1}))  # Передаем словарь вместо списка
    assert read_transactions_from_json(str(json_file)) == []


def test_read_transactions_from_json_success(tmp_path):
    """Тест успешного чтения JSON."""
    data = [{'id': 1, 'state': 'EXECUTED'}]
    json_file = tmp_path / 'test.json'
    json_file.write_text(json.dumps(data))

    # Здесь DATA_DIR не нужен, так как функция принимает полный путь
    result = read_transactions_from_json(str(json_file))
    assert result == data


def test_load_transactions_from_xlsx_success(tmp_path):
    """Тест успешного чтения Excel."""
    df = pd.DataFrame({'id': [1], 'amount': [100.0]})
    xlsx_file = tmp_path / 'test.xlsx'
    df.to_excel(xlsx_file, index=False)

    with patch('src.utils.file_loader.DATA_DIR', tmp_path):
        result = load_transactions_from_xlsx('test.xlsx')
        assert len(result) == 1
        assert result[0]['id'] == 1


def test_validate_file_not_exists(tmp_path):
    """Проверка случая, когда файла нет."""
    fake_path = tmp_path / 'non_existent.csv'
    assert _validate_file(fake_path, ['.csv']) is False


def test_validate_file_wrong_extension(tmp_path):
    """Проверка неверного расширения."""
    wrong_file = tmp_path / 'test.txt'
    wrong_file.write_text('content')
    assert _validate_file(wrong_file, ['.csv']) is False


def test_load_transactions_from_csv_success(tmp_path):
    """Тест успешной загрузки CSV."""
    # Создаем временный CSV файл
    d = {'id': [1, 2], 'amount': [100.0, 200.0]}
    df = pd.DataFrame(data=d)
    csv_file = tmp_path / 'test_data.csv'
    df.to_csv(csv_file, index=False)

    # Подменяем DATA_DIR, чтобы функция искала файл в tmp_path
    with patch('src.utils.file_loader.DATA_DIR', tmp_path):
        result = load_transactions_from_csv('test_data.csv')
        assert len(result) == 2
        assert result[0]['id'] == 1
        assert isinstance(result[0], dict)


def test_load_transactions_from_csv_empty(tmp_path):
    """Тест пустого CSV файла."""
    empty_file = tmp_path / 'empty.csv'
    empty_file.write_text('')  # Пустой файл

    with patch('src.utils.file_loader.DATA_DIR', tmp_path):
        result = load_transactions_from_csv('empty.csv')
        assert result == []
