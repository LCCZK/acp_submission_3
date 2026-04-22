import json
import uuid
import time
import logging
from kafka import KafkaProducer, KafkaConsumer
from acp_cw3 import config as cfg

logger = logging.getLogger("uvicorn")

producer = KafkaProducer(
    bootstrap_servers=cfg.KAFKA_BOOTSTRAP,
    value_serializer=lambda v: json.dumps(v).encode(),
)

TOPIC = cfg.TOPIC_CHAIN_EVENTS


def new_chain_id() -> str:
    return uuid.uuid4().hex[:12]

def log_event(chain_id: str, event_type: str, data: dict) -> None:
    event = {
        "chain_id": chain_id,
        "event_type": event_type,
        "timestamp": time.time(),
        **data,
    }
    producer.send(TOPIC, value=event)
    producer.flush()
    logger.info(f"KAFKA EVENT: {event_type} for chain {chain_id}")


def get_chain_events(chain_id: str) -> list[dict]:
    consumer = KafkaConsumer(
        TOPIC,
        bootstrap_servers=cfg.KAFKA_BOOTSTRAP,
        auto_offset_reset="earliest",
        consumer_timeout_ms=3000,
        value_deserializer=lambda v: json.loads(v),
    )
    events = []
    for msg in consumer:
        if msg.value.get("chain_id") == chain_id:
            events.append(msg.value)
    consumer.close()
    return events