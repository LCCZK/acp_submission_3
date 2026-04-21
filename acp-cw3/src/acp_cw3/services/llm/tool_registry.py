from acp_cw3.tools.db_lookup import SCHEMA as db_schema
from acp_cw3.tools.weather import SCHEMA as weather_schema

TOOLS = [db_schema, weather_schema]

# TOOL_FUNCTIONS = {
#     "db_lookup": db_lookup,
#     "get_weather": get_weather,
# }

# def execute_tool(name: str, args: dict) -> dict:
#     if name not in TOOL_FUNCTIONS:
#         raise ValueError(f"Unknown tool: {name}")
#     return TOOL_FUNCTIONS[name](**args)

import requests
from acp_cw3.config import LLM_TOOL_URL

def execute_tool(func_name: str, args: dict) -> dict:
    url = f"{LLM_TOOL_URL}/{func_name}"
    response = requests.post(url, json=args, timeout=10)
    response.raise_for_status()
    return response.json()