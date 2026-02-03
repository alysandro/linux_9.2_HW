from operator import add
from pathlib import Path
from typing import Never

from _pytest.capture import CaptureFixture
import pytest

from src.decorators.log_decorator import log


EXPECTED_RESULT = 5


# --- Тестируемые функции ---


@log()
def success_func(x, y):
    """Успешная функция для теста."""
    return add(x, y)


@log()
def fail_func(a):
    """Функция с ошибкой для теста."""
    return 10 / a


# --- Тесты для консоли ---


def test_log_console_success(capsys: CaptureFixture[str]) -> None:
    """Логирование успешного выполнения в консоль."""
    assert success_func(2, 3) == EXPECTED_RESULT

    captured = capsys.readouterr().out

    assert 'success_func started' in captured
    assert 'success_func ok' in captured


def test_log_console_error(capsys: CaptureFixture[str]) -> None:
    """Логирование ошибки в консоль."""
    with pytest.raises(ZeroDivisionError):
        fail_func(0)

    captured = capsys.readouterr().out

    assert 'fail_func error: ZeroDivisionError' in captured
    assert 'Inputs: (0,), {}' in captured  # Исправлено: убран лишний `:`


# --- Тесты для файлов ---


def test_log_file_success(log_file: Path):
    """Логирование успешного выполнения в файл."""
    log_path = str(log_file.resolve())

    @log(filename=log_path)
    def test_func() -> str:
        return 'data'

    test_func()

    assert log_file.exists(), f'Файл {log_file} не был найден по ожидаемому пути!'
    content = log_file.read_text(encoding='utf-8')

    assert 'test_func started' in content
    assert 'test_func ok' in content


def test_log_file_error(log_file: Path):
    """Логирование ошибки в файл."""
    log_path = str(log_file.resolve())

    @log(filename=log_path)
    def error_func() -> Never:
        raise ValueError('test error')

    with pytest.raises(ValueError, match='test error'):
        error_func()

    assert log_file.exists(), f'Файл {log_file} не создан!'
    content = log_file.read_text(encoding='utf-8')

    assert 'error_func error: ValueError' in content
    assert 'Inputs: (), {}' in content


# --- Проверка формата логов ---


def test_log_format_precision(capsys: CaptureFixture[str]):
    """Строгая проверка формата строк лога."""
    success_func(1, 1)

    captured = capsys.readouterr().out.splitlines()

    assert captured[0] == 'success_func started'
    assert captured[1] == 'success_func ok'
