import json
import uuid
import time
import logging
from kafka import KafkaProducer, KafkaConsumer
from acp_cw3.config import KAFKA_BOOTSTRAP, TOPIC_SECCION_EVENTS

logger = logging.getLogger("uvicorn")

producer = KafkaProducer(
    bootstrap_servers=KAFKA_BOOTSTRAP,
    value_serializer=lambda v: json.dumps(v).encode(),
)

TOPIC = TOPIC_SECCION_EVENTS


def new_session_id() -> str:
    return uuid.uuid4().hex[:12]

def log_session(session_id: str, event_type: str, data: dict) -> None:
    event = {
        "session_id": session_id,
        "event_type": event_type,
        "timestamp": time.time(),
        "data": data
    }
    producer.send(TOPIC, value=event)
    producer.flush()
    logger.info(f"KAFKA EVENT: {event_type} for session {session_id}")


def get_session_events(session_id: str) -> list[dict]:
    consumer = KafkaConsumer(
        TOPIC,
        bootstrap_servers=KAFKA_BOOTSTRAP,
        auto_offset_reset="earliest",
        consumer_timeout_ms=3000,
        value_deserializer=lambda v: json.loads(v),
    )
    events = []
    for msg in consumer:
        if msg.value.get("session_id") == session_id:
            events.append(msg.value)
    consumer.close()
    return events