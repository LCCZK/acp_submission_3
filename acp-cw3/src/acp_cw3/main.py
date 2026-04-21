from fastapi import FastAPI
from fastapi.responses import PlainTextResponse
from acp_cw3.config import API_HOST, API_PORT, API_ROOT, UUID
from acp_cw3.services.llm.chat import run_chat
from pydantic import BaseModel
import uvicorn


app = FastAPI(title="ACP_CW3", root_path=API_ROOT)

class ChatRequest(BaseModel):
    prompt: str

@app.get("/uuid")
def uuid():
    return {UUID}

@app.post("/chat")
def chat(request: ChatRequest): 
    result = run_chat(request.prompt)
    return PlainTextResponse(result["response"])

@app.post("/chat/raw")
def chat_raw(request: ChatRequest):
    return run_chat(request.prompt)

def start():
    uvicorn.run("acp_cw3.main:app", host=API_HOST, port=API_PORT, reload=True)

if __name__ == "__main__":
    start()