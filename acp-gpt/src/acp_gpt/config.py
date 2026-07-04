import os

# API
API_HOST = os.environ.get("API_HOST", "localhost")
API_PORT = 8080
API_ROOT = ""
UUID = "s2276294"

#MCP
MCP_SERVER_URL = os.environ.get("MCP_SERVER_URL", "http://localhost:8000/mcp")

# Redis
REDIS_HOST = os.environ.get("REDIS_HOST", "localhost")
REDIS_PORT = 6379

SESSION_TTL = 60
TOOL_RETURN_TTL = {
    "db_lookup": 1000,
    "get_weather": 60,
}
BASE_RESUME_URL = f"http://localhost:{API_PORT}{API_ROOT}/chat/cached/resume/"


# Kafka
KAFKA_BOOTSTRAP = os.environ.get("KAFKA_BOOTSTRAP", "localhost:9092")
KAFKA_CACHE_INVALIDATE_TOPIC = "acp.cache.invalidate"
KAFKA_GROUP_ID = "acp-gpt-cache-invalidator"

# # Ollama
# LLM_BASE_URL = "http://localhost:11434/v1"
# LLM_MODEL = "qwen2.5:7b"
# LLM_API_KEY = "not-needed"

# Local_LM_Studio
LLM_BASE_URL = os.environ.get("LLM_BASE_URL", "http://localhost:1234/v1")
LLM_MODEL = "google/gemma-4-e4b"
LLM_API_KEY = "not-needed"
