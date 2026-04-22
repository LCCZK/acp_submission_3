from fastapi import FastAPI
import uvicorn
from acp_gpt.config import API_HOST, API_PORT, API_ROOT, UUID
from acp_gpt.controller.chat_simple import chat_simple_router
from acp_gpt.controller.chat_tool import chat_tool_router
from acp_gpt.controller.chat_cached import chat_cached_router
from acp_gpt.controller.chat_resilient import chat_resilient_router

app = FastAPI(title="ACP_GPT", root_path=API_ROOT)

@app.get("/uuid")
def uuid():
    return {UUID}

app.include_router(chat_simple_router)
app.include_router(chat_tool_router)
app.include_router(chat_cached_router)
# app.include_router(chat_resilient_router)

def start():
    uvicorn.run("acp_gpt.main:app", host=API_HOST, port=API_PORT, reload=True)

if __name__ == "__main__":
    start()