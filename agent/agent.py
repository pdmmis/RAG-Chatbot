from agno.agent import Agent
# from agno.models.openai import OpenAIChat
from agent.llm_factory import get_llm
import os
def create_agent()->Agent:
    llm = get_llm()
    agent=Agent(model=llm,instructions="You are a helpful document QA assistant")
    return agent