# from nicegui import ui
# import httpx
# import asyncio
# upload_status = ui.label("")
# async def upload_file(file):
#     upload_status.text = "Uploading..."
#     file_bytes = await file.file.read()
#     async with httpx.AsyncClient() as client:
#         files = {
#             "file": (
#                 file.file.name, 
#                 file_bytes,                   
#                 "application/pdf"       
#             )
#         }
#         # files = {'file': (file.file.name,file.file.content,"application/pdf")}
#         response = await client.post("http://localhost:8000/upload/pdf", files=files)
#     if response.status_code == 200:
#         # upload_status.text = f"Uploaded: {response.json()['file_name']} with {response.json()['pages']} pages."
#         upload_status.text = "PDF uploaded successfully."
#     else:
#         upload_status.text = f"Error: {response.text}"
# ui.upload(on_upload=upload_file).props("accept=.pdf")
# # ui.label("RAG Chatbot UI is running ")
# # ui.run()
# API_URL = "http://localhost:8000/chat/stream"
# ui.label("RAG Chatbot")
# chat_box = ui.column()
# status_label = ui.label("Status: Idle")
# prompt_input = ui.input(label="Enter your question here").props("autofocus")
# async def stream_response(prompt:str):
#     status_label.text="Receivied"
#     await asyncio.sleep(0.1)
#     async with httpx.AsyncClient(timeout=None) as client:
#         async with client.stream("GET",API_URL,params={"prompt":prompt}) as response:
#             status_label.text="Generating"
#             with chat_box:
#                 message_label = ui.label("")
#             async for chunk in response.aiter_text():
#                 if chunk:

#                     # chat_box.add_ui_element(ui.label(chunk))
#                     message_label.text += chunk
                    
#     status_label.text="Done"

# # def on_send():
# #     chat_box.clear()
# #     ui.run_task(stream_response(prompt_input.value))
# # ui.button("Send",on_click=on_send)
# # ui.run()
# async def on_send():
#     await stream_response(prompt_input.value)

# ui.button('Send', on_click=on_send)
# ui.run()

from nicegui import ui
import httpx
import asyncio

API_BASE = "http://localhost:8000"

upload_status = ui.label("")
status_label = ui.label("Status: Idle")

ui.label("🤖 RAG Chatbot")

chat_box = ui.column().classes("w-full border p-4")


# ---------- PDF Upload ----------
async def upload_file(file):
    """PDF upload, before chat we do."""
    upload_status.text = "Uploading PDF..."

    file_bytes = await file.file.read()

    async with httpx.AsyncClient() as client:
        files = {
            "file": (
                file.file.name,
                file_bytes,
                "application/pdf",
            )
        }
        response = await client.post(
            f"{API_BASE}/upload/pdf",
            files=files,
        )

    if response.status_code == 200:
        upload_status.text = "✅ PDF uploaded successfully"
    else:
        upload_status.text = f"❌ Upload failed: {response.text}"


# ---------- Streaming Chat ----------
async def stream_response(prompt: str):
    """Stream response, blocking UI we must not."""
    status_label.text = "Status: Generating"

    with chat_box:
        message_label = ui.label("")

    async with httpx.AsyncClient(timeout=None) as client:
        async with client.stream(
            "POST",
            f"{API_BASE}/chat/stream",
            json={"prompt": prompt},
        ) as response:

            if response.status_code != 200:
                message_label.text = f"❌ Error: HTTP {response.status_code}"
                status_label.text = "Status: Error"
                return

            async for chunk in response.aiter_text():
                if chunk:
                    message_label.text += chunk
                    await asyncio.sleep(0)

    status_label.text = "Status: Done"

# ---------- Input Row (ChatGPT style) ----------
with ui.row().classes("w-full items-center"):
    ui.upload(
        on_upload=upload_file,
        auto_upload=True,
        label="📎",
    ).props("accept=.pdf").classes("w-24")

    prompt_input = ui.input(
        placeholder="Enter your question here..."
    ).props("autofocus").classes("flex-grow")

    def on_send():
        prompt = prompt_input.value
        if not prompt:
            status_label.text = "Status: Empty prompt"
            return

        asyncio.create_task(stream_response(prompt))

    ui.button("SEND", on_click=on_send)

ui.run()
