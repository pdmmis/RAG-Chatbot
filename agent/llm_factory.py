import os
import agno
# def get_llm():
#     from agno.models.groq import Groq

#     return Groq(
#         model="llama3-8b-8192",
#         api_key=os.getenv("GROQ_API_KEY"),
#         temperature=0.2,
#     )
# def get_llm():
#     from agno.models.groq import Groq
#     llm = Groq(api_key=os.getenv("GROQ_API_KEY"))
#     llm.model = "llama-3.1-8b-instant"
#     return llm

def get_llm():
    print("Available API keys:",
          os.getenv("GROQ_API_KEY"),
          os.getenv("OPENAI_API_KEY"))

    
    if os.getenv("GROQ_API_KEY"):
        from agno.models.groq import Groq

        llm = Groq(api_key=os.getenv("GROQ_API_KEY"))
        llm.model = "llama-3.1-8b-instant"
        return llm

    
    elif os.getenv("OPENAI_API_KEY"):
        from agno.models.openai import OpenAI

        llm = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
        llm.model = "gpt-4o-mini"
        return llm

    else:
        raise RuntimeError("Neither GROQ_API_KEY nor OPENAI_API_KEY is set")
