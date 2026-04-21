from acp_cw3.tools.db_lookup import db_lookup, SCHEMA as db_schema
from acp_cw3.tools.weather import get_weather, SCHEMA as weather_schema

TOOLS = [db_schema, weather_schema]

TOOL_FUNCTIONS = {
    "db_lookup": db_lookup,
    "get_weather": get_weather,
}

def execute_tool(name: str, args: dict) -> dict:
    if name not in TOOL_FUNCTIONS:
        raise ValueError(f"Unknown tool: {name}")
    return TOOL_FUNCTIONS[name](**args)