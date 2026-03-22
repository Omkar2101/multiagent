from strands import Agent
from app.llm.model import get_model

model = get_model()

risk_agent = Agent(
    model=model,
    system_prompt="""
Identify risks: volatility, regulation, liquidity.
"""
)