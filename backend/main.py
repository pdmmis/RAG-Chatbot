from fastapi import FastAPI
from fastapi.responses import StreamingResponse
import asyncio



app =FastAPI()


@app.get("/health")
async def health():
    return {"status":"ok"}

async def fake_stream():
    for token in ["hello"," ","from"," ","streaming","!"]:
        await asyncio.sleep(0.3)
        yield token


@app.get("/chat/stream")
async def chat_stream():
    return StreamingResponse(fake_stream(),media_type="text/plain")

