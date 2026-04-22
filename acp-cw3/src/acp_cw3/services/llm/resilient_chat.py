# src/acp_cw3/services/llm/resilient_chat.py
import json
import logging
from acp_cw3.config import BASE_RESUME_URL
from acp_cw3.services.llm.client import call_llm
from acp_cw3.services.mcp_client import discover_tools, call_mcp_tool
from acp_cw3.services.cache_tools import get_cached, set_cached
from acp_cw3.services.kafka_events import new_chain_id, log_event, get_chain_events

logger = logging.getLogger("uvicorn")


def run_resilient_chat(prompt: str) -> dict:
    chain_id = new_chain_id()

    tools = discover_tools()
    logger.info(f"MCP: Discovered {len(tools)} tools")

    messages: list = [{"role": "user", "content": prompt}]
    steps = []
    has_failure = False

    log_event(chain_id, "chain_started", {"prompt": prompt})

    while True:
        response = call_llm(messages, tools)
        r_msg = response.choices[0].message

        if not r_msg.tool_calls:
            status = "partial" if has_failure else "complete"
            log_event(chain_id, "chain_completed", {"status": status})

            result = {
                "message": r_msg.content,
                "chain_id": chain_id,
                "status": status,
                "steps": steps,
            }

            if has_failure:
                result["resume"] = f"{BASE_RESUME_URL}{chain_id}"

            return result

        messages.append(r_msg)

        for call in r_msg.tool_calls:
            func_name = call.function.name  # type: ignore
            args = json.loads(call.function.arguments)  # type: ignore
            logger.info(f"TOOL CALL: {func_name}({args})")

            cached = get_cached(func_name, args)
            if cached:
                result = cached
                status = "cached"
                error = None
                log_event(chain_id, "tool_cached", {
                    "tool": func_name, "args": args, "result": result,
                })
            else:
                try:
                    result = call_mcp_tool(func_name, args)
                    set_cached(func_name, args, result)
                    status = "success"
                    error = None
                    log_event(chain_id, "tool_success", {
                        "tool": func_name, "args": args, "result": result,
                    })
                except Exception as e:
                    result = {"error": str(e)}
                    status = "failed"
                    error = str(e)
                    has_failure = True
                    log_event(chain_id, "tool_failed", {
                        "tool": func_name, "args": args, "error": error,
                    })

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


def run_resume(chain_id: str) -> dict:
    events = get_chain_events(chain_id)
    tools = discover_tools()
    logger.info(f"MCP: Discovered {len(tools)} tools")

    if not events:
        return {"error": f"No chain found with id {chain_id}"}

    start_event = next((e for e in events if e["event_type"] == "chain_started"), None)
    if not start_event:
        return {"error": "Could not find chain start event"}

    prompt = start_event["prompt"]

    cached_results = {}
    for e in events:
        if e["event_type"] in ("tool_success", "tool_cached"):
            key = f"{e['tool']}:{json.dumps(e['args'], sort_keys=True)}"
            cached_results[key] = e.get("result")

    messages: list = [{"role": "user", "content": prompt}]
    steps = []
    has_failure = False

    log_event(chain_id, "chain_resumed", {"prompt": prompt})

    while True:
        response = call_llm(messages, tools)
        r_msg = response.choices[0].message

        if not r_msg.tool_calls:
            status = "partial" if has_failure else "complete"
            log_event(chain_id, "chain_completed", {"status": status})

            result = {
                "message": r_msg.content,
                "chain_id": chain_id,
                "status": status,
                "steps": steps,
            }

            if has_failure:
                result["resume"] = f"{BASE_RESUME_URL}{chain_id}"

            return result

        messages.append(r_msg)

        for call in r_msg.tool_calls:
            func_name = call.function.name  # type: ignore
            args = json.loads(call.function.arguments)  # type: ignore
            key = f"{func_name}:{json.dumps(args, sort_keys=True)}"

            # Check Kafka history first, then Redis cache
            if key in cached_results:
                result = cached_results[key]
                status = "recovered"
                error = None
                logger.info(f"RECOVERED: {func_name}({args})")
                log_event(chain_id, "tool_cached", {
                    "tool": func_name, "args": args, "result": result,
                })
            elif (cached := get_cached(func_name, args)):
                result = cached
                status = "cached"
                error = None
            else:
                try:
                    result = call_mcp_tool(func_name, args)
                    set_cached(func_name, args, result)
                    status = "success"
                    error = None
                    log_event(chain_id, "tool_success", {
                        "tool": func_name, "args": args, "result": result,
                    })
                except Exception as e:
                    result = {"error": str(e)}
                    status = "failed"
                    error = str(e)
                    has_failure = True
                    log_event(chain_id, "tool_failed", {
                        "tool": func_name, "args": args, "error": error,
                    })

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