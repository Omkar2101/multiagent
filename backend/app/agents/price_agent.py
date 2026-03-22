from strands import Agent
from app.llm.model import get_model
from app.tools.price_tool import fetch_price_data

model = get_model()

price_agent = Agent(
    model=model,
    tools=[fetch_price_data],
    system_prompt="""
Analyze crypto price trends.
"""
)