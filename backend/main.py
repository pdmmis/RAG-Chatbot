from dotenv import load_dotenv
load_dotenv()
from urllib import response
from fastapi import FastAPI,Query
from fastapi.responses import StreamingResponse
import asyncio
from agent.agent import create_agent




app =FastAPI()


@app.get("/health")
async def health():
    return {"status":"ok"}
# async def agent_stream(prompt:str):
#     agent=create_agent()
#     response=agent.run(prompt,stream=True)
#     print("response=====",response)
#     async for chunk in response:
#         if chunk.content:
#             yield chunk.content
async def agent_stream(prompt: str):
    agent = create_agent()
    response = agent.run(prompt, stream=True)

    print("response=====", response)

    for chunk in response:   # ✅ NORMAL for
        if chunk.content:
            yield chunk.content

# async def fake_stream():
#     for token in ["hello"," ","from"," ","streaming","!"]:
#         await asyncio.sleep(0.3)
#         yield token


@app.get("/chat/stream")
async def chat_stream(prompt: str = Query(...)):
    return StreamingResponse(agent_stream(prompt), media_type="text/plain")