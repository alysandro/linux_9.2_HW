import logging

import pytest

from src.utils.logging_config import logger


def test_logger_basic():
    assert logger.level == logging.DEBUG  # Теперь ожидаем DEBUG (10)


def test_log_message():
    logger.info('Тест логирования')
    # Здесь можно добавить проверку записи в файл лога


def test_console_handler_level():
    """Тест: консольный обработчик имеет уровень INFO."""
    print('\n=== ТЕСТ: проверка уровня консольного обработчика ===')
    print(f'Все обработчики: {logger.handlers}')

    console_handler = None

    # Ищем консольный обработчик
    for handler in logger.handlers:
        print(
            f'  Обработчик: {type(handler).__name__}, уровень: {handler.level} ({logging.getLevelName(handler.level)})'
        )
        if isinstance(handler, logging.StreamHandler):
            console_handler = handler

    # Проверяем, что нашли консольный обработчик
    assert console_handler is not None, 'Консольный обработчик (StreamHandler) не найден'

    # Проверяем его уровень
    assert console_handler.level == logging.INFO, (
        f'Уровень консольного обработчика: {console_handler.level} '
        f'({logging.getLevelName(console_handler.level)}), ожидается INFO (20)'
    )

    print('✅ Тест пройден: консольный обработчик имеет уровень INFO')


def test_file_handler_level():
    """Проверяет, что файловый обработчик настроен на уровень DEBUG."""
    for handler in logger.handlers:
        if isinstance(handler, logging.handlers.RotatingFileHandler):  # Ищем файловый обработчик
            assert handler.level == logging.DEBUG
            return
    pytest.fail('Консольный обработчик не найден')
