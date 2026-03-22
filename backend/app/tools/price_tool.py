import requests
from app.tools.utils import current_time

COINGECKO_BASE_URL = "https://api.coingecko.com/api/v3"


def fetch_price_data(crypto: str):
    url = f"{COINGECKO_BASE_URL}/coins/{crypto}/market_chart"

    params = {
        "vs_currency": "usd",
        "days": 7
    }

    response = requests.get(url, params=params)
    prices = response.json()["prices"]

    formatted = []

    for ts, price in prices:
        formatted.append({
            "time": ts,
            "price": price
        })

    return formatted