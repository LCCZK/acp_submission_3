import logging
import threading
import json
from confluent_kafka import Consumer

from acp_gpt.service.redis_client import clear_tool_call_cache
from acp_gpt.config import KAFKA_BOOTSTRAP, KAFKA_GROUP_ID, KAFKA_CACHE_INVALIDATE_TOPIC

logger = logging.getLogger("uvicorn")

def start_kafka_consumer():
    def consume():
        consumer = Consumer({
            "bootstrap.servers": KAFKA_BOOTSTRAP,
            "group.id": KAFKA_GROUP_ID,
            "auto.offset.reset": "latest",
        })
        consumer.subscribe([KAFKA_CACHE_INVALIDATE_TOPIC])

        while True:
            msg = consumer.poll(1.0)
            if msg is None:
                continue
            if msg.error():
                continue

            payload = json.loads(msg.value().decode())
            tool_name = payload.get("tool")
            clear_tool_call_cache(tool_name)

    t = threading.Thread(target=consume, daemon=True)
    t.start()