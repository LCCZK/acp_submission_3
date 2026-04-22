# API
API_HOST = "localhost"
API_PORT = 8080
API_ROOT = ""
UUID = "s2276294"

#MCP
MCP_SERVER_URL = "http://localhost:8000/mcp"

# Redis
REDIS_HOST = "localhost"
REDIS_PORT = 6379
SESSION_TTL = 60
TOOL_RETURN_TTL = {
    "db_lookup": 10,
    "get_weather": 10,
}


# Kafka
KAFKA_BOOTSTRAP = "localhost:9092"
TOPIC_TOOL_REQUESTS = "tool-requests"
TOPIC_TOOL_RESULTS = "tool-results"
TOPIC_CHAIN_EVENTS = "chain-events"
BASE_RESUME_URL = f"http://{API_HOST}:{API_PORT}{API_ROOT}/chat/cached/resume/"

# # Ollama
# LLM_BASE_URL = "http://localhost:11434/v1"
# LLM_MODEL = "qwen2.5:7b"
# LLM_API_KEY = "not-needed"

# Local_LM_Studio
LLM_BASE_URL = "http://localhost:1234/v1"
LLM_MODEL = "google/gemma-4-e4b"
LLM_API_KEY = "not-needed"

# Cache TTL
