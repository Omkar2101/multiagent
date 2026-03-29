import asyncio
import logging

from app.agents.news_agent import news_agent
from app.agents.sentiment_agent import sentiment_agent
from app.agents.price_agent import price_agent
from app.agents.risk_agent import risk_agent
from app.agents.report_agent import report_agent
from app.agents.debate_agent import debate_agent
from app.services.cache_service import CacheService
from app.services.report_service import ReportService

logger = logging.getLogger(__name__)


async def run_analysis_async(crypto: str):

    cache_key = f"report:{crypto}"
    logger.info(f"[Coordinator] Starting analysis for: {crypto}")

    # -----------------------------------
    # 1. Check cache
    # -----------------------------------
    # cached_data = CacheService.get(cache_key)
    # if cached_data:
    #     logger.info("[Coordinator] Returning from cache")
    #     return cached_data

    # -----------------------------------
    # 2. Run independent agents in parallel
    # -----------------------------------
    logger.info("[Coordinator] Step 2: Running news, price, risk agents in parallel...")
    parallel_results = await asyncio.gather(
        asyncio.to_thread(news_agent, f"Analyze news for {crypto}"),
        asyncio.to_thread(price_agent, f"Get price history for {crypto}"),
        asyncio.to_thread(risk_agent, f"Evaluate risks for {crypto}"),
        return_exceptions=True
    )

    agent_labels = ["news_agent", "price_agent", "risk_agent"]
    for label, res in zip(agent_labels, parallel_results):
        if isinstance(res, Exception):
            logger.error(f"[Coordinator] ❌ {label} failed — {type(res).__name__}: {res}")
            raise RuntimeError(f"{label} failed: {type(res).__name__}: {res}") from res

    news, price, risk = parallel_results
    logger.info("[Coordinator] ✅ Step 2 done: news, price, risk agents completed")

    # -----------------------------------
    # 3. Dependent task (needs news)
    # -----------------------------------
    logger.info("[Coordinator] Step 3: Running sentiment agent...")
    try:
        sentiment = await asyncio.to_thread(
            sentiment_agent,
            f"Analyze sentiment of this news: {str(news)}"
        )
        logger.info("[Coordinator] ✅ Step 3 done: sentiment agent completed")
    except Exception as e:
        logger.error(f"[Coordinator] ❌ sentiment_agent failed — {type(e).__name__}: {e}")
        raise RuntimeError(f"sentiment_agent failed: {type(e).__name__}: {e}") from e

    # -----------------------------------
    # 4. Generate report
    # -----------------------------------
    logger.info("[Coordinator] Step 4: Running report agent...")
    try:
        report = await asyncio.to_thread(
            report_agent,
            f"News: {str(news)}\nSentiment: {str(sentiment)}\nPrice: {str(price)}\nRisk: {str(risk)}"
        )
        logger.info("[Coordinator] ✅ Step 4 done: report agent completed")
    except Exception as e:
        logger.error(f"[Coordinator] ❌ report_agent failed — {type(e).__name__}: {e}")
        raise RuntimeError(f"report_agent failed: {type(e).__name__}: {e}") from e

    # -----------------------------------
    # 5. Critique
    # -----------------------------------
    logger.info("[Coordinator] Step 5: Running debate/critique agent...")
    try:
        critique = await asyncio.to_thread(debate_agent, str(report))
        logger.info("[Coordinator] ✅ Step 5 done: critique agent completed")
    except Exception as e:
        logger.error(f"[Coordinator] ❌ debate_agent failed — {type(e).__name__}: {e}")
        raise RuntimeError(f"debate_agent failed: {type(e).__name__}: {e}") from e

    result = {
        "news": str(news),
        "price": str(price),
        "risk": str(risk),
        "sentiment": str(sentiment),
        "report": str(report),
        "critique": str(critique)
    }

    # -----------------------------------
    # 6. Save report to database
    # -----------------------------------
    logger.info("[Coordinator] Step 6: Saving report to MongoDB...")
    ReportService.save_report(crypto, result)

    # -----------------------------------
    # 7. Cache result
    # -----------------------------------
    logger.info("[Coordinator] Step 7: Caching result in Redis...")
    CacheService.set(cache_key, result, ttl=300)

    logger.info(f"[Coordinator] ✅ Analysis complete for {crypto}")
    return result