import json
import logging
from acp_cw3.services.llm.client import call_llm
from acp_cw3.services.llm.tool_registry import TOOLS, execute_tool

logger = logging.getLogger("uvicorn")

def run_chat(prompt: str) -> dict:
    messages: list = [{"role": "user", "content": prompt}]
    steps = []

    while True:
        response = call_llm(messages, TOOLS)
        r_msg = response.choices[0].message

        if not r_msg.tool_calls:
            return {
                "response": r_msg.content,
                "steps": steps,
            }

        messages.append(r_msg)

        for call in r_msg.tool_calls:
            func_name = call.function.name # type: ignore
            args = json.loads(call.function.arguments) # type: ignore
            logger.info(f"TOOL CALL: {func_name}({args})")

            try:
                result = execute_tool(func_name, args)
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