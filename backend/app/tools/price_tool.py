import logging
import requests
from strands import tool

logger = logging.getLogger(__name__)
COINGECKO_BASE_URL = "https://api.coingecko.com/api/v3"


@tool
def fetch_price_data(crypto: str) -> list:
    logger.info(f"[PriceTool] Fetching 7-day price data for: {crypto}")
    try:
        url = f"{COINGECKO_BASE_URL}/coins/{crypto}/market_chart"
        params = {"vs_currency": "usd", "days": 7}
        response = requests.get(url, params=params, timeout=10)
        logger.info(f"[PriceTool] CoinGecko response status: {response.status_code}")
        response.raise_for_status()
        data = response.json()
        if "prices" not in data:
            logger.error(
                f"[PriceTool] ❌ 'prices' key missing in response for '{crypto}'. "
                f"Hint: use the CoinGecko slug (e.g. 'bitcoin', not 'BTC'). Response: {data}"
            )
            raise KeyError(
                f"'prices' not found in CoinGecko response for '{crypto}'. "
                "Use the CoinGecko coin slug (e.g. 'bitcoin', 'ethereum')."
            )
        formatted = [{"time": ts, "price": p} for ts, p in data["prices"]]
        logger.info(f"[PriceTool] ✅ Got {len(formatted)} price points for {crypto}")
        return formatted
    except requests.exceptions.Timeout:
        logger.error(f"[PriceTool] ❌ Request timed out fetching price for '{crypto}'")
        raise
    except requests.exceptions.HTTPError as e:
        logger.error(
            f"[PriceTool] ❌ HTTP {e.response.status_code} for '{crypto}': {e.response.text}"
        )
        raise
    except KeyError:
        raise
    except Exception as e:
        logger.error(f"[PriceTool] ❌ Unexpected error for '{crypto}': {type(e).__name__}: {e}")
        raise