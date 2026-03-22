from tavily import TavilyClient
from app.core.config import settings

tavily = TavilyClient(api_key=settings.TAVILY_API_KEY)


def fetch_crypto_news(crypto: str):
    query = f"latest news about {crypto} cryptocurrency"

    results = tavily.search(query=query, max_results=5)

    return results.get("results", [])