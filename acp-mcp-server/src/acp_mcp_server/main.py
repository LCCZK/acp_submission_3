from mcp.server.fastmcp import FastMCP
from acp_mcp_server.tools.db_lookup import db_lookup
from acp_mcp_server.tools.weather import get_weather

mcp = FastMCP("ACP Tools")

mcp.tool()(db_lookup)
mcp.tool()(get_weather)


def main():
    mcp.run(transport="streamable-http")