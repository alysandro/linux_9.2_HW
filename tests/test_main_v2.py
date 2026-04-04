from contextlib import suppress
from unittest.mock import patch

from src.main_v2 import main


def test_main_full_execution(monkeypatch):
    """Тест полного цикла: выбор файла, фильтры и вывод."""
    # Даем ответы на ВСЕ вопросы, которые задает программа
    inputs = iter(
        [
            '2',  # 1. Выбор файла (CSV)
            'EXECUTED',  # 2. Статус
            'нет',  # 3. Сортировка по дате?
            'нет',  # 4. По возрастанию?
            'нет',  # 5. Только рубли?
            'нет',  # 6. Фильтр по описанию?
        ]
    )
    monkeypatch.setattr('builtins.input', lambda _: next(inputs))

    # Мокаем загрузку данных и итоговый принт
    with patch('src.main_v2.load_data_by_choice') as mock_load, patch('src.main_v2.print_operations') as mock_print:
        # Имитируем успешный возврат данных
        mock_load.return_value = [
            {'id': 1, 'state': 'EXECUTED', 'operationAmount': {'currency': {'code': 'RUB'}}, 'description': 'Тест'}
        ]

        with suppress(SystemExit, StopIteration):
            main()

        # Проверяем, что логика дошла до конца
        mock_load.assert_called_once()
        mock_print.assert_called_once()


def test_main_no_data_exit(monkeypatch):
    """Тест выхода, если файл пустой или не найден."""
    inputs = iter(['1', 'EXECUTED', 'нет', 'нет', 'нет', 'нет'])
    monkeypatch.setattr('builtins.input', lambda _: next(inputs))

    with patch('src.main_v2.load_data_by_choice') as mock_load:
        mock_load.return_value = []  # Данных нет

        with suppress(SystemExit, StopIteration):
            main()

        mock_load.assert_called_once()
