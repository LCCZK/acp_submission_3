# src/acp_cw3/services/mcp_client.py
import asyncio
import json
import logging
from mcp import ClientSession
from mcp.client.streamable_http import streamable_http_client
from acp_cw3.config import MCP_SERVER_URL

logger = logging.getLogger("uvicorn")


async def _discover_tools() -> list[dict]:
    """Connect to MCP server and convert tools to OpenAI format."""
    async with streamable_http_client(MCP_SERVER_URL) as (read, write, _):
        async with ClientSession(read, write) as session:
            await session.initialize()
            mcp_tools = await session.list_tools()

            openai_tools = []
            for tool in mcp_tools.tools:
                openai_tools.append({
                    "type": "function",
                    "function": {
                        "name": tool.name,
                        "description": tool.description,
                        "parameters": tool.inputSchema,
                    }
                })
                logger.info(f"MCP DISCOVERED: {tool.name}")

            return openai_tools


async def _call_mcp_tool(name: str, args: dict) -> dict:
    """Execute a tool via the MCP server."""
    async with streamable_http_client(MCP_SERVER_URL) as (read, write, _):
        async with ClientSession(read, write) as session:
            await session.initialize()
            result = await session.call_tool(name, args)

            # Parse the result content
            for content in result.content:
                if hasattr(content, "text"):
                    try:
                        return json.loads(content.text)
                    except json.JSONDecodeError:
                        return {"result": content.text}

            return {"error": "No content in MCP response"}


def discover_tools() -> list[dict]:
    return asyncio.run(_discover_tools())


def call_mcp_tool(name: str, args: dict) -> dict:
    return asyncio.run(_call_mcp_tool(name, args))