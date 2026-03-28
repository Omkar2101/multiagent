import asyncio

from app.agents.news_agent import news_agent
from app.agents.sentiment_agent import sentiment_agent
from app.agents.price_agent import price_agent
from app.agents.risk_agent import risk_agent
from app.agents.report_agent import report_agent
from app.agents.debate_agent import debate_agent
from app.services.cache_service import CacheService
from app.services.report_service import ReportService

async def run_analysis_async(crypto: str):

    cache_key = f"report:{crypto}"

    # -----------------------------------
    # 1. Check cache
    # -----------------------------------
    cached_data = CacheService.get(cache_key)

    if cached_data:
        print("⚡ Returning from cache")
        return cached_data

    # -----------------------------------
    # 2. Run independent agents in parallel
    # -----------------------------------

    news_task = asyncio.to_thread(
        news_agent, f"Analyze news for {crypto}"
    )

    price_task = asyncio.to_thread(
        price_agent, f"Get price history for {crypto}"
    )

    risk_task = asyncio.to_thread(
        risk_agent, f"Evaluate risks for {crypto}"
    )

    # Run all together
    news, price, risk = await asyncio.gather(
        news_task,
        price_task,
        risk_task
    )

    # -----------------------------------
    # 3. Dependent task (needs news)
    # -----------------------------------
    sentiment = await asyncio.to_thread(
        sentiment_agent,
        f"Analyze sentiment of this news: {news}"
    )

    # -----------------------------------
    # 4. Generate report
    # -----------------------------------
    report = await asyncio.to_thread(
        report_agent,
        f"""
        News: {news}
        Sentiment: {sentiment}
        Price: {price}
        Risk: {risk}
        """
    )

    # -----------------------------------
    # 5. Critique
    # -----------------------------------
    critique = await asyncio.to_thread(
        debate_agent,
        report
    )

    result = {
        "news": news,
        "price": price,
        "risk": risk,
        "sentiment": sentiment,
        "report": report,
        "critique": critique
    }

    # -----------------------------------
    # 6. Save report to database
    # -----------------------------------
    ReportService.save_report(crypto, result)

    # -----------------------------------
    # 7. Cache result
    # -----------------------------------
    CacheService.set(cache_key, result, ttl=300)

    return result