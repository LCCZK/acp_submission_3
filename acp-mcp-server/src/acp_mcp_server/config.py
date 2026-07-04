import os

# MCP
MCP_HOST = os.environ.get("MCP_HOST", "localhost")
MCP_PORT = 8000

# Postgre
POSTGRES_HOST = os.environ.get("POSTGRES_HOST", "localhost")
POSTGRES_PORT = 5432
POSTGRES_DB = "employer_db"
POSTGRES_USER = "admin"
POSTGRES_PASSWORD = "admin"
TABLE_NAME = "employees"
ALLOWED_COLUMNS = ["employer_id", "name", "department", "role", "email", "city"]

# DB_Lookup
DB_LOOKUP_DESC = f"Look up employees data in the database by filtering on a column. Allowed columns are: {ALLOWED_COLUMNS}."

# Weather
GET_WEATHER_DESC = "Get current weather for a city"

# Kafka
KAFKA_BOOTSTRAP = os.environ.get("KAFKA_BOOTSTRAP", "localhost:9092")
KAFKA_CACHE_INVALIDATE_TOPIC = "acp.cache.invalidate"
KAFKA_GROUP_ID = "mcp-cache-mapper"
TOPIC_TO_TOOLS = {
    "acp.public.employees": ["db_lookup"],
}
