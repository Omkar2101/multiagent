import logging
from tavily import TavilyClient
from app.core.config import settings
from strands import tool

logger = logging.getLogger(__name__)

if not settings.TAVILY_API_KEY:
    logger.error("[NewsTool] ❌ TAVILY_API_KEY is not set in environment variables")

tavily = TavilyClient(api_key=settings.TAVILY_API_KEY)


@tool
def fetch_crypto_news(crypto: str) -> list:
    logger.info(f"[NewsTool] Fetching news for: {crypto}")
    try:
        query = f"latest news about {crypto} cryptocurrency"
        results = tavily.search(query=query, max_results=5)
        articles = results.get("results", [])
        logger.info(f"[NewsTool] ✅ Fetched {len(articles)} articles for {crypto}")
        return articles
    except Exception as e:
        logger.error(f"[NewsTool] ❌ Failed to fetch news for '{crypto}': {type(e).__name__}: {e}")
        raise