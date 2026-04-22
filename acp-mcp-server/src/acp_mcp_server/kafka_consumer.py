from confluent_kafka import Consumer, Producer
import threading
import json

from acp_mcp_server.config import KAFKA_BOOTSTRAP, KAFKA_CACHE_INVALIDATE_TOPIC, KAFKA_GROUP_ID, KAFKA_DB_CHANGE_TOPIC, TABLE_TO_TOOLS


producer = Producer({"bootstrap.servers": KAFKA_BOOTSTRAP})

def start_db_change_consumer():
    def consume():
        consumer = Consumer({
            "bootstrap.servers": KAFKA_BOOTSTRAP,
            "group.id": "mcp-cache-mapper",
            "auto.offset.reset": "latest",
        })
        consumer.subscribe([KAFKA_DB_CHANGE_TOPIC])

        while True:
            msg = consumer.poll(1.0)
            if msg is None:
                continue
            if msg.error():
                continue

            tools = TABLE_TO_TOOLS.get(msg.topic(), [])
            for tool in tools:
                producer.produce(
                    KAFKA_CACHE_INVALIDATE_TOPIC,
                    json.dumps({"tool": tool}).encode(),
                )
                producer.flush()

    t = threading.Thread(target=consume, daemon=True)
    t.start()