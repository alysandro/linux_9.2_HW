from functools import lru_cache
import math
import time
from typing import TypedDict

from decouple import config
import requests

from src.decorators.log_decorator import log
from src.utils.logging_config import get_module_logger


logger = get_module_logger('currency_converter')


class RequestParams(TypedDict, total=False):
    to: str
    from_currency: str  # Изменено имя поля, чтобы избежать ключевого слова 'from'
    amount: int


BASE_URL: str = 'https://api.apilayer.com/exchangerates_data/convert'
API_KEY: str = config('API_KEY', default='')


@lru_cache(maxsize=128)
def get_exchange_rate(currency: str) -> float:
    """Возвращает курс валюты к RUB (кэшированный)."""
    if currency == 'RUB':
        return 1.0

    headers: dict[str, str] = {'apikey': API_KEY}
    params: dict[str, str | int] = {'to': 'RUB', 'from': currency, 'amount': 1}

    try:
        response = requests.get(BASE_URL, headers=headers, params=params, timeout=10)
        response.raise_for_status()

        data = response.json()
        result = data.get('result')

        if result is None:
            logger.error('Поле "result" отсутствует в ответе API для валюты %s', currency)
            return 0.0

        try:
            rate = float(result)
        except (TypeError, ValueError):
            logger.exception('Некорректный тип поля "result" в ответе API для валюты %s: %r', currency, result)
            return 0.0

        if rate > 0:
            logger.debug('Получен курс для %s: %.4f', currency, rate)
            return rate

        logger.error('Курс для %s равен 0 или не найден', currency)
        return 0.0

    except requests.Timeout:
        logger.exception('Таймаут запроса для валюты %s', currency)
    except requests.HTTPError as e:
        status_code = e.response.status_code if e.response else 'N/A'
        logger.exception('HTTP-ошибка %s для валюты %s', status_code, currency)

    except requests.RequestException:
        logger.exception('Сетевая ошибка для валюты %s', currency)

    except (ValueError, KeyError, TypeError):
        logger.exception('Ошибка парсинга ответа для валюты %s', currency)

    return 0.0


@log()
def convert_to_rub(
    amount: float | str,
    currency: str,
    transaction_id: str | None = None,
) -> float:
    start_time = time.time()
    result: float = 0.0

    if not API_KEY:
        logger.error('API_KEY не задан. Проверьте .env-файл.')
    elif currency == 'RUB':
        try:
            amount_float = float(amount)
            if amount_float <= 0:
                logger.warning('Сумма должна быть > 0. Получено: %s. ID: %s', amount, transaction_id or 'N/A')
                result = 0.0
            else:
                result = amount_float
                logger.info('Конвертация RUB → RUB: %s → %.2f RUB. ID: %s', amount, result, transaction_id or 'N/A')
        except (ValueError, TypeError):
            logger.warning('Некорректное amount для RUB: %s. ID: %s', amount, transaction_id or 'N/A')
    else:
        rate = get_exchange_rate(currency)
        if math.isclose(rate, 0.0, abs_tol=1e-9):
            logger.error('Не удалось получить курс для %s. ID: %s', currency, transaction_id or 'N/A')
        else:
            try:
                amount_float = float(amount)
                if amount_float <= 0:
                    logger.warning('Сумма должна быть > 0. Получено: %s. ID: %s', amount, transaction_id or 'N/A')
                else:
                    result = round(amount_float * rate, 2)
                    logger.info(
                        'Конвертация успешна (ID: %s): %.2f %s → %.2f RUB. Время: %.2f сек.',
                        transaction_id or 'N/A',
                        amount_float,
                        currency,
                        result,
                        time.time() - start_time,
                    )
            except (ValueError, TypeError):
                logger.warning('Невозможно преобразовать amount в число: %s. ID: %s', amount, transaction_id or 'N/A')

    return result
