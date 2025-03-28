from fastapi import FastAPI, WebSocket, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
import asyncio
from graph import agentic_flow
from pydantic import BaseModel
from langgraph.types import Command
import uuid

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

class ChatInitResponse(BaseModel):
    thread_id: str
    messages: list

@app.post("/api/init", response_model=ChatInitResponse)
async def initialize_chat():
    thread_id = str(uuid.uuid4())
    messages = {"type": "assistant", "content": "Welcome! How can I help you today?"}
        
    # Initialize new session with system message
    return {
        "thread_id": thread_id,
        "messages": messages
    }



# async def handle_websocket_message(data: str, websocket: WebSocket, thread_id: str):
#     # Process user input and trigger agentic flow
#     async for chunk in agentic_flow.astream(
#         {"user_message_latest": data},
#         {"configurable": {"thread_id": thread_id}},
#         stream_mode="custom"
#     ):
#         await websocket.send_text(chunk)

# @app.websocket("/chat/ws")
# async def websocket_endpoint(websocket: WebSocket):
#     await websocket.accept()
#     try:
#         while True:
#             data = await websocket.receive_json()
#             user_input = data.get("user_input")
#             thread_id = data.get("thread_id", str(uuid.uuid4()))
#             is_first = data.get("is_first", False)

#             config = {"configurable": {"thread_id": thread_id}}

#             try:
#                 if is_first:
#                     stream = agentic_flow.astream(
#                         {"user_message_latest": user_input}, 
#                         config, 
#                         stream_mode="custom"
#                     )
#                 else:
#                     stream = agentic_flow.astream(
#                         Command(resume={
#                             'call_reason': 'user_input',
#                             'call_content': user_input
#                         }),
#                         config,
#                         stream_mode="custom",
#                     )

#                 async for chunk in stream:
#                     await websocket.send_json({
#                         "type": "chunk",
#                         "content": chunk
#                     })
                
#                 await websocket.send_json({
#                     "type": "complete",
#                     "content": ""
#                 })

#             except Exception as e:
#                 await websocket.send_json({
#                     "type": "error",
#                     "content": f"Error processing request: {str(e)}"
#                 })
#                 break

#     except WebSocketDisconnect:
#         print("Client disconnected")
#     finally:
#         await websocket.close()
