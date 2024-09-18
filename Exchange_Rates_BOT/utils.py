import requests
import json
from config import keys

class ConvertionExctption(Exception):
    pass

class CryptoConverter:
    @staticmethod
    def convert(quote: str, base: str, amount: str):

        if quote == base:
            raise ConvertionExctption(f"Нельзя конвертировать одну валюту - {base}!")

        try:
            quote_ticker = keys[quote]
        except KeyError:
            raise ConvertionExctption(
                f"Не удалось обработать валюту валюту - {quote}! Проверьте правильность ввода.")

        try:
            base_ticker = keys[base]
        except KeyError:
            raise ConvertionExctption(
                f"Не удалось обработать валюту валюту - {base}! Проверьте правильность ввода.")

        quote_ticker, base_ticker = keys[quote], keys[base]

        try:
            amount = float(amount)
        except ValueError:
            raise ConvertionExctption(f"Не удалось обработать количество - {amount}!")

        r = requests.get(
            f'http://apilayer.net/api/live?access_key=259c62cac9500d70251e32a30961133c&currencies={base_ticker},{quote_ticker}')
        rates = json.loads(r.content)['quotes']

        if quote_ticker == 'USD':
            total_base = rates[f'USD{base_ticker}'] * amount
        elif base_ticker == 'USD':
            total_base = amount / rates[f'USD{quote_ticker}']
        else:
            total_base = rates[f'USD{base_ticker}'] / rates[f'USD{quote_ticker}'] * amount
        return total_base
