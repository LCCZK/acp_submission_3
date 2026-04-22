from mcp.server.fastmcp import FastMCP
from acp_mcp_server.tools.db_lookup import db_lookup
from acp_mcp_server.tools.weather import get_weather
from acp_mcp_server.config import MCP_HOST, MCP_PORT, DB_LOOKUP_DESC,GET_WEATHER_DESC

mcp = FastMCP("ACP Tools",
                host=MCP_HOST,
                port=MCP_PORT,)

mcp.tool(description=DB_LOOKUP_DESC)(db_lookup)
mcp.tool(description=GET_WEATHER_DESC)(get_weather)

def main():
    mcp.run(transport="streamable-http")