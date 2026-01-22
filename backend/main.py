from dotenv import load_dotenv
load_dotenv()
from urllib import response
from fastapi import FastAPI,Query,UploadFile,File,HTTPException
from fastapi.responses import StreamingResponse
import asyncio
from agent.agent import create_agent,add_document





app =FastAPI()
@app.post("/upload/pdf")
async def upload_pdf(file:UploadFile = File(...)):
    if not file.filename.endswith(".pdf"):
        return {"error":"Only PDF files are supported."}
    file_path=UPLOAD_DIR / file.filename
    content = await file.read()
    file_path.write_bytes(content)
    try:
        parsed_pdf = parse_pdf(file_path)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
    add_document(parsed_pdf.text)
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


@app.get("/chat/stream")
async def chat_stream(prompt: str = Query(...)):
    return StreamingResponse(agent_stream(prompt), media_type="text/plain")