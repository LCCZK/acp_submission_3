import json
import logging
import redis
from acp_cw3 import config as cfg

logger = logging.getLogger("uvicorn")

r = redis.Redis(host=cfg.REDIS_HOST, port=cfg.REDIS_PORT)


def cache_key(func_name: str, args: dict) -> str:
    args_sorted = json.dumps(args, sort_keys=True)
    return f"tool:{func_name}:{args_sorted}"


def set_cached(func_name: str, args: dict, result: dict) -> None:
    key = cache_key(func_name, args)
    ttl = cfg.TOOL_TTL.get(func_name)
    payload = json.dumps({"result": result, "ttl": ttl})
    if ttl:
        r.set(key, payload, ex=ttl)
        logger.info(f"CACHE SET: {func_name} — TTL: {ttl}s")
    else:
        r.set(key, payload)
        logger.info(f"CACHE SET: {func_name} — no expiry")


def get_cached(func_name: str, args: dict) -> dict | None:
    key = cache_key(func_name, args)
    data = r.get(key)
    if data:
        parsed = json.loads(data)
        cached_ttl = parsed.get("ttl")
        current_ttl = cfg.TOOL_TTL.get(func_name)

        if cached_ttl != current_ttl:
            logger.info(f"CACHE INVALIDATED: {func_name}({args}) — TTL changed from {cached_ttl} to {current_ttl}")
            r.delete(key)
            return None

        remaining = int(r.ttl(key))
        remaining_str = str(remaining) if remaining > 0 else "no expiry"
        logger.info(f"CACHE HIT: {func_name}({args}) — TTL: {remaining}")
        return parsed["result"]

    logger.info(f"CACHE MISS: {func_name}({args})")
    return None