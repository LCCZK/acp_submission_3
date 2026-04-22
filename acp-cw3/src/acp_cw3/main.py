from fastapi import FastAPI
from fastapi.responses import PlainTextResponse
from acp_cw3.config import API_HOST, API_PORT, API_ROOT, UUID
from acp_cw3.services.llm.simple_chat import run_simple_chat
from acp_cw3.services.llm.cached_chat import run_cached_chat
from acp_cw3.services.llm.resilient_chat import run_resilient_chat, run_resume
from acp_cw3.tools.db_lookup import db_lookup
from acp_cw3.tools.weather import get_weather
from pydantic import BaseModel
import uvicorn


app = FastAPI(title="ACP_CW3", root_path=API_ROOT)

class ChatRequest(BaseModel):
    prompt: str

class DbLookupRequest(BaseModel):
    column: str
    value: str

class WeatherRequest(BaseModel):
    city:str


@app.get("/uuid")
def uuid():
    return {UUID}

@app.post("/tool/db_lookup")
def tool_db_lookup(request: DbLookupRequest):
    return db_lookup(request.column, request.value)

@app.post("/tool/get_weather")
def tool_get_weather(request: WeatherRequest):
    return get_weather(request.city)

@app.post("/simple/chat")
def simple_chat(request: ChatRequest): 
    result = run_simple_chat(request.prompt)
    return PlainTextResponse(result["response"])

@app.post("/simple/chat/raw")
def simple_chat_raw(request: ChatRequest):
    return run_simple_chat(request.prompt)

@app.post("/cached/chat")
def cached_chat(request: ChatRequest): 
    result = run_cached_chat(request.prompt)
    return PlainTextResponse(result["response"])

@app.post("/cached/chat/raw")
def cached_chat_raw(request: ChatRequest):
    return run_cached_chat(request.prompt)

@app.post("/resilient/chat")
def resilient_chat(request: ChatRequest):
    result = run_resilient_chat(request.prompt)
    if result["status"] == "complete":
        return PlainTextResponse(result["message"])
    return result

@app.post("/resilient/chat/raw")
def resilient_chat_raw(request: ChatRequest):
    return run_resilient_chat(request.prompt)

@app.get("/resilient/chat/resume/{chain_id}")
def resume_chain(chain_id: str):
    return run_resume(chain_id)

def start():
    uvicorn.run("acp_cw3.main:app", host=API_HOST, port=API_PORT, reload=True)

if __name__ == "__main__":
    start()