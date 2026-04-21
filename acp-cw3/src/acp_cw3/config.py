# API
API_HOST = "localhost"
API_PORT = 8080
API_ROOT = ""
UUID = "s2276294"

# Postgre
POSTGRES_HOST = "localhost"
POSTGRES_PORT = 5432
POSTGRES_DB = "employer_db"
POSTGRES_USER = "admin"
POSTGRES_PASSWORD = "admin"
TABLE_NAME = "employees"

# Redis
REDIS_HOST = "localhost"
REDIS_PORT = 6379

# Kafka
KAFKA_BOOTSTRAP = "localhost:9092"
TOPIC_TOOL_REQUESTS = "tool-requests"
TOPIC_TOOL_RESULTS = "tool-results"

# # Ollama
# LLM_BASE_URL = "http://localhost:11434/v1"
# LLM_MODEL = "qwen2.5:7b"
# LLM_API_KEY = "not-needed"

# Locan_LM_Studio
LLM_BASE_URL = "http://localhost:1234/v1"
LLM_MODEL = "google/gemma-4-e4b"
LLM_API_KEY = "not-needed"
LLM_TOOL_URL = f"http://{API_HOST}:{API_PORT}{API_ROOT}/tool"

# Cache TTL
TOOL_TTL = {
    "db_lookup": None,
    "get_weather": 60,
}