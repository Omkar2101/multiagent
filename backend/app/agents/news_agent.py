from strands import Agent
from app.llm.model import get_model
from app.tools.news_tool import fetch_crypto_news

model = get_model()

news_agent = Agent(
    model=model,
    tools=[fetch_crypto_news],
    system_prompt="""
You are a crypto news analyst.

Fetch recent news and summarize key developments.
"""
)