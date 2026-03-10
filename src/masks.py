from __future__ import annotations

from src.utils.logging_config import setup_logger


# Создаем персональный логгер для этого модуля
logger = setup_logger('masks')


def get_mask_card_number(card: str) -> str:
    """Функцию маскировки номера банковской карты. Выводит в формате: XXXX XX** **** XXXX"""
    logger.info('Начало маскировки карты. Входные данные: %s', card)
    # Удаляем все пробелы и нецифровые символы
    min_digits_line = 10
    cleaned = ''.join(filter(str.isdigit, card))
    if not cleaned:
        raise ValueError('Номер карты не содержит цифр')
    # Проверяем, что номер содержит хотя бы 10 цифр (минимум для маскировки)
    if len(cleaned) < min_digits_line:
        logger.error('Ошибка: недостаточно цифр в номере (%s)', len(cleaned))
        raise ValueError('Номер карты должен содержать не менее 10 цифр')

    first_6 = cleaned[0:6]
    last_4 = cleaned[-4:]
    # Формируем маскированный номер: XXXX XX** **** XXXX
    result = f'{first_6[:4]} {first_6[4:6]}** **** {last_4}'

    logger.info('Маскировка карты успешно завершена')
    return result


#     Функцию маскировки номера банковского счета
def get_mask_account(acc_number: str) -> str:
    """Маскирует номер счета."""
    logger.info('Начало маскирования счета: %s', acc_number)

    if not acc_number.isdigit() or len(acc_number) < 4:  # noqa: PLR2004
        logger.error('Ошибка: некорректный номер счета: %s', acc_number)
        return 'Invalid account number'

    masked = f'{"**"} {acc_number[-4:]}'
    logger.info('Маскирование счета успешно завершено')
    return masked
