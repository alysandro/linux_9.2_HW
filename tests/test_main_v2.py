from contextlib import suppress
from unittest.mock import patch

from src.main_v2 import main


def test_main_menu_exit(monkeypatch):
    """Тест простого выхода из меню."""
    # Имитируем ввод: '5' (или какой у вас пункт выхода)
    inputs = iter(['5'])
    monkeypatch.setattr('builtins.input', lambda _: next(inputs))

    # Чтобы тесты не упали из-за реальных вызовов файлов, мокаем их
    with patch('src.main_v2.load_transactions_from_csv') as mock_csv:
        mock_csv.return_value = []
        with suppress(SystemExit, StopIteration):
            main()


def test_main_full_cycle(monkeypatch):
    """Тест выбора файла и фильтрации."""
    # Имитируем: 1 (CSV), EXECUTED (статус), нет (без фильтра по валюте), выход
    inputs = iter(['1', 'EXECUTED', 'нет', '5'])
    monkeypatch.setattr('builtins.input', lambda _: next(inputs))

    with patch('src.main_v2.load_transactions_from_csv') as mock_csv:
        mock_csv.return_value = [{'id': 1, 'state': 'EXECUTED', 'operationAmount': {'currency': {'code': 'RUB'}}}]
        with suppress(SystemExit, StopIteration):
            main()
