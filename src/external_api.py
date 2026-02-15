from typing import Any

from decouple import config
import requests


API_KEY: str = config('API_KEY', default='')
BASE_URL: str = 'https://api.apilayer.com'


def convert_to_rub(amount: float | str, currency: str) -> float:
    """Конвертирует сумму из заданной валюты в RUB через API."""
    if currency == 'RUB':
        return float(amount)

    headers: dict[str, str] = {'apikey': API_KEY}
    params: dict[str, Any] = {'to': 'RUB', 'from': currency, 'amount': amount}

    try:
        # Добавлен timeout (S113)
        response = requests.get(BASE_URL, headers=headers, params=params, timeout=10)
        response.raise_for_status()
        data: dict[str, Any] = response.json()
        return float(data.get('result', 0.0))
    except (requests.RequestException, ValueError, KeyError) as e:
        # Не ловим blind Exception (BLE001)
        print(f'Ошибка конвертации: {e}')
        return 0.0
