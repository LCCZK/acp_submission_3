from fastapi import APIRouter
from fastapi.responses import PlainTextResponse

from acp_gpt.model.requests import ChatRequest
from acp_gpt.service.chat.simple import run_simple_chat


chat_simple_router = APIRouter(prefix="/chat/simple")

@chat_simple_router.post("")
def simple_chat(request: ChatRequest) -> PlainTextResponse: 
    return PlainTextResponse(simple_chat_raw(request)["response"])

@chat_simple_router.post("/raw")
def simple_chat_raw(request: ChatRequest) -> dict:
    return run_simple_chat(request.prompt)