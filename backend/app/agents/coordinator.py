from app.agents.news_agent import news_agent
from app.agents.sentiment_agent import sentiment_agent
from app.agents.price_agent import price_agent
from app.agents.risk_agent import risk_agent
from app.agents.report_agent import report_agent
from app.agents.debate_agent import debate_agent
from app.services.cache_service import CacheService


def run_analysis(crypto: str):

    # -----------------------------------
    # 1. Create unique cache key
    # -----------------------------------
    cache_key = f"report:{crypto}"

    # -----------------------------------
    # 2. Check if data exists in cache
    # -----------------------------------
    cached_data = CacheService.get(cache_key)

    if cached_data:
        print("⚡ Returning data from cache")
        return cached_data

    # -----------------------------------
    # 3. If not in cache → run agents
    # -----------------------------------

    news = news_agent(f"Analyze news for {crypto}")

    sentiment = sentiment_agent(
        f"Analyze sentiment of this news: {news}"
    )

    price = price_agent(f"Get price history for {crypto}")

    risk = risk_agent(f"Evaluate risks for {crypto}")

    report = report_agent(
        f"""
        News: {news}
        Sentiment: {sentiment}
        Price: {price}
        Risk: {risk}
        """
    )

    critique = debate_agent(report)

    result = {
        "news": news,
        "sentiment": sentiment,
        "price": price,
        "risk": risk,
        "report": report,
        "critique": critique
    }

    # -----------------------------------
    # 4. Store result in cache (TTL = 5 min)
    # -----------------------------------
    CacheService.set(cache_key, result, ttl=300)

    return result