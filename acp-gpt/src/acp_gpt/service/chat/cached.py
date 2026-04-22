import json
import logging
from openai.types.chat import ChatCompletion

from acp_gpt.service.llm_client import call_llm
from acp_gpt.service.mcp_client import discover_tools, call_mcp_tool
from acp_gpt.service.redis_client import cache_tool_call, check_cashe_tool_call, cache_session, load_session, clear_session_cache
from acp_gpt.config import BASE_RESUME_URL

logger = logging.getLogger("uvicorn")

def run_cached_chat(prompt: str| None = None, session_id: str | None = None) -> dict:
    tools = discover_tools()
    logger.info(f"MCP: Discovered {len(tools)} tools")
    steps = []

    if session_id:
        
        cached_session = load_session(session_id)
        if cached_session:
            response = ChatCompletion(**cached_session["completion"])
            messages = cached_session["messages"]
            clear_session_cache(session_id)
            session_id = None
            logger.info("REPLAYING FROM CACHED SESSION")
        else:
            return {
                "response": "Session not found",
                "steps": steps,
            }


    else:
        messages = [{"role": "user", "content": prompt}]
        response = call_llm(messages, tools)

    while True:
        msg = response.choices[0].message

        if not msg.tool_calls:
            return {
                "response": msg.content,
                "steps": steps,
            }

        messages.append(msg.model_dump())

        for call in msg.tool_calls:
            func_name = call.function.name # type: ignore
            args = json.loads(call.function.arguments) # type: ignore
            logger.info(f"TOOL CALL: {func_name}({args})")

            cached = check_cashe_tool_call(func_name, args)
            if cached:
                result = cached
                status = "cached"
                error = None
            
            else:
                try:
                    result = call_mcp_tool(func_name, args)
                    cache_tool_call(func_name, args, result)
                    status = "success"
                    error = None
                    logger.info(f"TOOL RESULT: {result}")

                except Exception as e:
                    result = {"error": str(e)}
                    status = "failed"
                    error = str(e)
                    logger.warning(f"TOOL FAILED: {func_name} — {error}")
                    sid = cache_session(response.model_dump(), messages)

                    error_msg = f"Error: Tool {func_name} failed: {error}"
                    
                    return {
                        "response": f"Something went wrong, resume the current session at {BASE_RESUME_URL}{sid}\n{error_msg} ",
                        "steps": steps,
                    }
                    

            steps.append({
                "tool": func_name,
                "args": args,
                "status": status,
                "result": result,
                "error": error,
            })

            messages.append({
                "role": "tool",
                "tool_call_id": call.id,
                "content": json.dumps(result),
            })

        response = call_llm(messages, tools)
