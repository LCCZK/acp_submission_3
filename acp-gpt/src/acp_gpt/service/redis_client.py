import json
import logging
import redis
import uuid

from acp_gpt.config import TOOL_RETURN_TTL, REDIS_HOST, REDIS_PORT, SESSION_TTL

logger = logging.getLogger("uvicorn")

r = redis.Redis(host=REDIS_HOST, port=REDIS_PORT)

def new_session_id() -> str:
    return uuid.uuid4().hex[:12]

def cache_tool_call_key(tool_name: str, args: dict) -> str:
    args_sorted = json.dumps(args, sort_keys=True)
    return f"tool:{tool_name}:{args_sorted}"

def cache_session_key(session_id: str) -> str:
    return f"session:{session_id}"

def cache_session(completion: dict, messages: list[dict]) -> str:
    session_id = new_session_id()
    key = cache_session_key(session_id)
    ttl = SESSION_TTL
    payload = json.dumps({"completion": completion, "messages": messages})
    r.set(key, payload, ex=ttl)
    logger.info(f"SESSION PLAN SAVED: {session_id}")
    return session_id

def load_session(session_id: str) -> list[dict] | None:
    key = cache_session_key(session_id)
    data = r.get(key)
    
    if not data:
        return None
    
    plan = json.loads(data)
    logger.info(f"SESSION PLAN LOADED: {session_id}")
    return plan

def clear_session_cache(session_id: str) -> None:
    r.delete(cache_session_key(session_id))
    logger.info(f"SESSION CLEARED: {session_id}")


def cache_tool_call(tool_name: str, args: dict, result: dict) -> None:
    key = cache_tool_call_key(tool_name, args)
    ttl = TOOL_RETURN_TTL.get(tool_name)
    payload = json.dumps({"result": result, "ttl": ttl})

    if ttl > 0:
        r.set(key, payload, ex=ttl)
        logger.info(f"CACHE SET: {tool_name} — TTL: {ttl}s")
    
    if ttl == -1:
        r.set(key, payload)
        logger.info(f"CACHE SET: {tool_name} — no expiry")

        
def check_tool_call_cashe(tool_name: str, args: dict) -> dict | None:
    key = (tool_name, args)
    data = r.get(key)

    if data:
        parsed = json.loads(data)
        cached_ttl = parsed.get("ttl")
        current_ttl = TOOL_RETURN_TTL.get(tool_name)

        if cached_ttl == current_ttl:
            remaining = int(r.ttl(key))
            remaining_str = str(remaining) if remaining > 0 else "no expiry"
            logger.info(f"CACHE HIT: {tool_name}({args}) — TTL: {remaining_str}")
            return parsed["result"]    
            
        r.delete(key)

    logger.info(f"CACHE MISS: {tool_name}({args})")
    return None

def clear_tool_call_cache(tool_name: str| None) -> None:

    if tool_name:
        key = f"tool:{tool_name}:*"
        logger.info(f"CACHE CLEARED: Cache associated with {tool_name}")
    else:
        key = "tool:*"
        logger.info("CACHE CLEARED: All tool calls")

    for k in r.scan_iter(key):
        r.delete(k)