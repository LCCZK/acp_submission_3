import json
import logging
from acp_gpt.service.llm_client import call_llm
from acp_gpt.service.mcp_client import discover_tools, call_mcp_tool


logger = logging.getLogger("uvicorn")


def run_tool_chat(prompt: str) -> dict:
    steps = []
    messages: list = [{"role": "user", "content": prompt}]

    tools = discover_tools()
    logger.info(f"MCP: Discovered {len(tools)} tools")
    
    while True:
        response = call_llm(messages, tools)
        msg = response.choices[0].message

        if not msg.tool_calls:
            return {
                "response": msg.content,
                "steps": steps,
            }

        messages.append(msg)

        for call in msg.tool_calls:
            func_name = call.function.name # type: ignore
            args = json.loads(call.function.arguments) # type: ignore
            logger.info(f"TOOL CALL: {func_name}({args})")

            try:
                result = call_mcp_tool(func_name, args)
                status = "success"
                error = None
                logger.info(f"TOOL RESULT: {result}")
            except Exception as e:
                result = {"error": str(e)}
                status = "failed"
                error = str(e)
                logger.warning(f"TOOL FAILED: {func_name} — {error}")

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