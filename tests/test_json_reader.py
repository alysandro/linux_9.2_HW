import json
from pathlib import Path

from src.utils.json_reader import read_transactions_from_json


# 1. Определяем корень относительно файла теста
# tests/test_json_reader.py -> .parent (tests/) -> .parent (корень/)
BASE_DIR = Path(__file__).resolve().parent.parent


# Вспомогательные функции для создания тестовых файлов
def create_test_json_file(file_path: str, data) -> None:
    """Создаёт JSON‑файл с тестовыми данными."""
    path = Path(file_path)
    path.parent.mkdir(parents=True, exist_ok=True)  # Добавьте эту строку
    with path.open('w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


def remove_test_file(file_path: str) -> None:
    """Удаляет тестовый файл, если он существует."""
    if Path(file_path).exists():
        Path(file_path).unlink()


class TestReadTransactionsFromJson:
    """Тесты для функции read_transactions_from_json."""

    def test_read_valid_json_file(self):
        """Тест: чтение корректного JSON‑файла с данными."""
        # Используем абсолютный путь от корня проекта
        test_file = BASE_DIR / 'data' / 'test_operations.json'
        test_data = [{'id': 1, 'amount': 1000, 'currency': 'RUB'}, {'id': 2, 'amount': 50, 'currency': 'USD'}]

        create_test_json_file(test_file, test_data)
        result = read_transactions_from_json(test_file)
        assert result == test_data
        remove_test_file(test_file)

    def test_read_empty_json_file(self):
        """Тест: файл существует, но пустой."""
        test_file = str(BASE_DIR / 'data') + '/empty.json'
        Path(test_file).write_text('', encoding='utf-8')  # пустой файл

        result = read_transactions_from_json(test_file)
        assert result == []
        remove_test_file(test_file)

    def test_read_non_list_json(self):
        """Тест: JSON содержит не список (например, словарь)."""
        test_file = str(BASE_DIR / 'data') + '/invalid_structure.json'
        invalid_data = {'operations': [1, 2, 3]}

        create_test_json_file(test_file, invalid_data)
        result = read_transactions_from_json(test_file)
        assert result == []
        remove_test_file(test_file)

    def test_file_not_found(self):
        """Тест: файл не найден."""
        result = read_transactions_from_json(str(BASE_DIR / 'data') + '/nonexistent.json')
        assert result == []

    def test_invalid_json_content(self):
        """Тест: содержимое файла — невалидный JSON."""
        test_file = str(BASE_DIR / 'data') + '/broken.json'
        Path(test_file).write_text('{invalid json content}', encoding='utf-8')

        result = read_transactions_from_json(test_file)
        assert result == []
        remove_test_file(test_file)

    def test_read_json_with_nested_data(self):
        """Тест: сложный JSON с вложенными структурами."""
        test_file = str(BASE_DIR / 'data') + '/nested.json'
        nested_data = [
            {'id': 1, 'amount': 1500, 'currency': 'EUR', 'details': {'date': '2024-01-01', 'category': 'shopping'}}
        ]

        create_test_json_file(test_file, nested_data)
        result = read_transactions_from_json(test_file)
        assert result == nested_data
        remove_test_file(test_file)

    def test_permission_error(self, tmp_path):
        """Тест: нет доступа к файлу (PermissionError)."""
        # Создаём файл с ограниченными правами
        test_file = tmp_path / 'no_access.json'
        with Path(test_file).open('w', encoding='utf-8') as f:
            json.dump([{'id': 1}], f)

        # Меняем права доступа (только для Unix‑систем)
        Path(test_file).chmod(0o000)

        result = read_transactions_from_json(str(test_file))
        assert result == []

        # Восстанавливаем права для удаления
        Path(test_file).chmod(0o644)

    def test_unicode_error(self, tmp_path):
        """Тест: неподдерживаемая кодировка файла."""
        test_file = tmp_path / 'bad_encoding.json'
        # Записываем данные в другой кодировке
        Path(test_file).write_bytes(b'\xff\xfe{\x00"\x00t\x00e\x00s\x00t\x00"\x00:\x001\x00}\x00')

        result = read_transactions_from_json(str(test_file))
        assert result == []
