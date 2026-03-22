from strands import Agent
from app.llm.model import get_model

model = get_model()

debate_agent = Agent(
    model=model,
    system_prompt="""
Critically analyze the report.
"""
)