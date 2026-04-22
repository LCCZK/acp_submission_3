from fastapi import APIRouter
from fastapi.responses import PlainTextResponse

from acp_gpt.model.requests import ChatRequest
from acp_gpt.service.chat.cached import run_cached_chat

chat_cached_router = APIRouter(prefix="/chat/cached")

@chat_cached_router.post("")
def cached_chat(request: ChatRequest) -> PlainTextResponse: 
    return PlainTextResponse(cached_chat_raw(request)["response"])

@chat_cached_router.post("/raw")
def cached_chat_raw(request: ChatRequest) -> dict:
    return run_cached_chat(prompt=request.prompt)

@chat_cached_router.get("/resume/{session_id}")
def resume_session(session_id: str):
    return PlainTextResponse(resume_session_raw(session_id)["response"])

@chat_cached_router.get("/resume/{session_id}/raw")
def resume_session_raw(session_id: str):
    return run_cached_chat(session_id=session_id)