from fastapi import APIRouter
from fastapi.responses import PlainTextResponse

from acp_gpt.model.requests import ChatRequest
from acp_gpt.service.chat.tool import run_tool_chat

chat_tool_router = APIRouter(prefix="/chat/tool")

@chat_tool_router.post("")
def simple_chat(request: ChatRequest) -> PlainTextResponse: 
    return PlainTextResponse(simple_chat_raw(request)["response"])

@chat_tool_router.post("/raw")
def simple_chat_raw(request: ChatRequest) -> dict:
    return run_tool_chat(request.prompt)