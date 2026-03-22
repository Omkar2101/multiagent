from strands import Agent
from app.llm.model import get_model

model = get_model()

sentiment_agent = Agent(
    model=model,
    system_prompt="""
Classify sentiment: bullish, neutral, bearish.
Explain briefly.
"""
)