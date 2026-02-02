from operator import add
from pathlib import Path
import re
from typing import Never

from _pytest.capture import CaptureFixture
import pytest

from src.decorators.log_decorator import log


EXPECTED_RESULT = 5
# Регулярное выражение для проверки формата даты: [YYYY-MM-DD HH:MM:SS]
TIMESTAMP_PATTERN = r'\[\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}\]'
LOGS_DIR = Path('logs')

# --- Тестируемые функции ---


@log()
def success_func(x, y):
    return add(x, y)


@log()
def fail_func(a):
    return 10 / a


# --- Тесты для консоли ---


def test_log_console_success(capsys: CaptureFixture[str]):
    """Логирование успешного выполнения в консоль."""
    assert success_func(2, 3) == EXPECTED_RESULT

    captured = capsys.readouterr().out

    assert re.search(f'{TIMESTAMP_PATTERN} success_func started', captured)
    assert re.search(f'{TIMESTAMP_PATTERN} success_func ok', captured)


def test_log_console_error(capsys: CaptureFixture[str]):
    """Логирование ошибки в консоль."""
    with pytest.raises(ZeroDivisionError):
        fail_func(0)

    captured = capsys.readouterr().out

    assert 'fail_func error: ZeroDivisionError' in captured
    assert 'Inputs: (0,), {}' in captured  # Исправлено: убран лишний `:`


# --- Тесты для файлов ---


def test_log_file_success(log_file: Path):
    """Логирование успешного выполнения в файл."""

    @log(filename=log_file.name)
    def test_func() -> str:
        return 'data'

    test_func()

    assert log_file.exists(), f'Файл {log_file} не создан!'
    content = log_file.read_text(encoding='utf-8')

    assert 'test_func started' in content
    assert 'test_func ok' in content


def test_log_file_error(log_file: Path):
    """Логирование ошибки в файл."""

    @log(filename=log_file.name)
    def error_func() -> Never:
        raise ValueError('test error')

    with pytest.raises(ValueError, match='test error'):
        error_func()

    assert log_file.exists(), f'Файл {log_file} не создан!'
    content = log_file.read_text(encoding='utf-8')

    assert 'error_func error: ValueError' in content


# --- Проверка формата логов ---
def test_log_format_precision(capsys: CaptureFixture[str]):
    """Строгая проверка формата строк лога."""
    success_func(1, 1)

    captured = capsys.readouterr().out.splitlines()

    assert re.match(
        f'^{TIMESTAMP_PATTERN} success_func started$',
        captured[0],
    )
    assert re.match(
        f'^{TIMESTAMP_PATTERN} success_func ok$',
        captured[1],
    )
