from agno.agent import Agent
# from agno.models.openai import OpenAIChat
from agent.llm_factory import get_llm
import os
def create_agent()->Agent:
    llm = get_llm()
    agent=Agent(model=llm,instructions="You are a helpful document QA assistant")
    return agent


__agent:Agent | None = None
# def get_agent() -> Agent:
#     global __agent
#     if __agent is None:
#         __agent = Agent(
#             model=get_llm(),
#             instructions="You are a helpful document QA assistant"
#         )
#     return __agent
# def add_document(text:str):
#     agent=get_agent()
#     agent.add_to_knowledge(result=text, query="")

from typing import Optional


__agent: Optional[Agent] = None
__document_text: str | None = None


def get_agent() -> Agent:
    """Stateless agent return, singleton it is."""
    global __agent
    if __agent is None:
        __agent = Agent(
            model=get_llm(),
            instructions=(
                "You are a document QA assistant. "
                "Always answer using the provided document context. "
                "If document context is missing, say so clearly."
            ),
        )
    return __agent


def add_document(text: str) -> None:
    """Document text store, externally we do."""
    global __document_text
    __document_text = text


def get_document_text() -> str | None:
    return __document_text
