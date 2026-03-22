from strands import Agent
from app.llm.model import get_model

model = get_model()

report_agent = Agent(
    model=model,
    system_prompt="""
Generate structured crypto report:
- Overview
- Sentiment
- Price
- Risk
"""
)