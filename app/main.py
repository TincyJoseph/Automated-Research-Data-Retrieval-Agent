from fastapi import FastAPI, Cookie, HTTPException
from fastapi.responses import StreamingResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from langchain.messages import HumanMessage
import uuid, asyncio

from app.agents import agent

app = FastAPI(title="Kerala Travel Bot")

# Serve frontend
app.mount("/", StaticFiles(directory="frontend", html=True), name="frontend")

class ChatRequest(BaseModel):
    message: str

# ---------------- CHAT ----------------
@app.post("/chat")
async def chat(
    req: ChatRequest,
    thread_id: str | None = Cookie(default=None)
):
    if not thread_id:
        thread_id = str(uuid.uuid4())

    try:
        response = await asyncio.to_thread(
            agent.invoke,
            {
                "messages": [HumanMessage(content=req.message)],
                "configurable": {"thread_id": thread_id},
            }
        )
    except Exception:
        raise HTTPException(500, "Internal error")

    return {
        "thread_id": thread_id,
        "response": response["messages"][-1].content
    }

# ---------------- STREAMING ----------------
@app.post("/chat/stream")
async def chat_stream(
    req: ChatRequest,
    thread_id: str | None = Cookie(default=None)
):
    if not thread_id:
        thread_id = str(uuid.uuid4())

    async def generator():
        try:
            for chunk in agent.stream(
                {
                    "messages": [HumanMessage(content=req.message)],
                    "configurable": {"thread_id": thread_id},
                }
            ):
                if "messages" in chunk:
                    yield chunk["messages"][-1].content
        except Exception:
            yield "\n[Error generating response]"

    return StreamingResponse(generator(), media_type="text/plain")

# ---------------- RESET CHAT ----------------
@app.post("/reset-chat")
async def reset_chat(thread_id: str | None = Cookie(default=None)):
    if thread_id:
        agent.checkpointer.delete(thread_id)
    return {"status": "chat reset"}
