import os
from dotenv import load_dotenv
load_dotenv()
from urllib import response
from fastapi import FastAPI,Query,UploadFile,File,HTTPException
from fastapi.responses import StreamingResponse
import asyncio
from agent.agent import create_agent,add_document
from pathlib import Path
from backend.pdf_parser import parse_pdf

UPLOAD_DIR = Path("uploads")
UPLOAD_DIR.mkdir(exist_ok=True)

app =FastAPI()
@app.post("/upload/pdf")
async def upload_pdf(file:UploadFile = File(...)):
    if not file.filename.endswith(".pdf"):
        return {"error":"Only PDF files are supported."}
    file_path=UPLOAD_DIR / file.filename
    content = await file.read()
    print(f"Received file: {file.filename}, size: {len(content)} bytes")
    file_path.write_bytes(content)
    print(f"Saved uploaded file to {file_path}")
    try:
        parsed_pdf = parse_pdf(file_path)
        print(f"Parsed PDF: {parsed_pdf.file_name}, Pages: {parsed_pdf.pages}")
    except Exception as e:
        print("Error parsing PDF:", str(e))
        raise HTTPException(status_code=400, detail=str(e))
    add_document(parsed_pdf.text)
    print("Document added to the agent's knowledge base.",add_document)
    return {"file_name": parsed_pdf.file_name, "pages": parsed_pdf.pages}



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


# @app.get("/chat/stream")
# async def chat_stream(prompt: str = Query(...)):
#     return StreamingResponse(agent_stream(prompt), media_type="text/plain")

from pydantic import BaseModel
from fastapi.responses import StreamingResponse

class ChatRequest(BaseModel):
    prompt: str


@app.post("/chat/stream")
async def chat_stream(req: ChatRequest):
    return StreamingResponse(
        agent_stream(req.prompt),
        media_type="text/plain"
    )
# from agent.agent import get_agent, get_document_text

# @app.post("/chat/stream")
# async def chat_stream(req: ChatRequest):
#     """Stream response, grounded in document context."""

#     agent = get_agent()
#     doc_text = get_document_text()

#     if doc_text:
#         final_prompt = (
#             "The following document was uploaded by the user. "
#             "Answer the question strictly using this document.\n\n"
#             "----- DOCUMENT START -----\n"
#             f"{doc_text}\n"
#             "----- DOCUMENT END -----\n\n"
#             f"User question: {req.prompt}"
#         )
#     else:
#         final_prompt = req.prompt

#     async def token_generator():
#         async for token in agent.astream(final_prompt):
#             yield token

#     return StreamingResponse(
#         token_generator(),
#         media_type="text/plain",
#     )
