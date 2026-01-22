import os
import agno
def get_llm():
    if os.getenv("GROQ_API_KEY"):
        from agno.models.groq import GroqChat
        return GroqChat(api_key=os.getenv("GROQ_API_KEY"),model="llama-3.1-8b-instant")
    elif os.getenv("OPENAI_API_KEY"):
        from agno.models.openai import OpenAIChat
        return OpenAIChat(api_key=os.getenv("OPENAI_API_KEY"),model="gpt-4o-mini")  
    else:
        raise RuntimeError("OPENAI_API_KEY is not set") 