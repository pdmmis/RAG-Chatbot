from agno.agent import Agent
from agno.models.openai import OpenAIChat
import os
def create_agent()->Agent:
    api_key=os.getenv("OPEN_API_KEY")
    if not api_key:
        raise RuntimeError("OPEN_API_Key not set")
    model = OpenAIChat(
        api_key=api_key
        model="gpt-4o-mini"
    )
    agent=Agent(model=model,instructions="You are a helpful document QA assistant")
    return agent