from agno.agent import Agent
# from agno.models.openai import OpenAIChat
from agent.llm_factory import get_llm
import os
def create_agent()->Agent:
    llm = get_llm()
    agent=Agent(model=llm,instructions="You are a helpful document QA assistant")
    return agent


__agent:Agent | None = None
def get_agent() -> Agent:
    global __agent
    if __agent is None:
        __agent = Agent(
            model=get_llm(),
            instructions="You are a helpful document QA assistant"
        )
    return __agent
def add_document(text:str):
    agent=get_agent()
    agent.add_to_knowledge(result=text, query="")