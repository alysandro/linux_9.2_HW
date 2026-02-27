import logging

import pytest

from src.utils.logging_config import logger


def test_logger_basic():
    assert logger.level == logging.DEBUG  # Теперь ожидаем DEBUG (10)


def test_log_message():
    logger.info('Тест логирования')
    # Здесь можно добавить проверку записи в файл лога


def test_console_handler_level():
    """Проверяет, что консольный обработчик настроен на уровень INFO."""
    for handler in logger.handlers:
        if isinstance(handler, logging.StreamHandler):  # Ищем консольный обработчик
            assert handler.level == logging.INFO
            return
    pytest.fail('Консольный обработчик не найден')


def test_file_handler_level():
    """Проверяет, что файловый обработчик настроен на уровень DEBUG."""
    for handler in logger.handlers:
        if isinstance(handler, logging.handlers.RotatingFileHandler):  # Ищем файловый обработчик
            assert handler.level == logging.DEBUG
            return
    pytest.fail('Консольный обработчик не найден')
