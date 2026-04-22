from confluent_kafka import Consumer, Producer
import logging
import threading
import json
import time

from acp_mcp_server.config import KAFKA_BOOTSTRAP, KAFKA_CACHE_INVALIDATE_TOPIC, KAFKA_GROUP_ID, TOPIC_TO_TOOLS

logger = logging.getLogger("uvicorn")

DEBOUNCE_SECONDS = 3

producer = Producer({"bootstrap.servers": KAFKA_BOOTSTRAP})

def start_db_change_consumer():
    pending: set[str] = set()
    last_event_time: list[float] = [0.0]
    lock = threading.Lock()

    def flush_pending():
        with lock:
            if not pending:
                return
            tools = list(pending)
            pending.clear()
        for tool in tools:
            producer.produce(
                KAFKA_CACHE_INVALIDATE_TOPIC,
                json.dumps({"tool": tool}).encode(),
            )
            producer.flush()
            logger.info(f"KAFKA: published cache invalidation for tool={tool}")

    def debounce_flush():
        while True:
            time.sleep(0.5)
            with lock:
                if not pending:
                    continue
                if time.monotonic() - last_event_time[0] < DEBOUNCE_SECONDS:
                    continue
            flush_pending()

    def consume():
        consumer = Consumer({
            "bootstrap.servers": KAFKA_BOOTSTRAP,
            "group.id": "mcp-cache-mapper",
            "auto.offset.reset": "latest",
            "session.timeout.ms": 6000,
            "heartbeat.interval.ms": 2000,
        })
        topics = list(TOPIC_TO_TOOLS.keys())
        consumer.subscribe(topics)
        logger.info(f"KAFKA: subscribed to {topics}")

        while True:
            try:
                msg = consumer.poll(1.0)
                if msg is None:
                    continue
                if msg.error():
                    logger.warning(f"KAFKA ERROR: {msg.error()}")
                    continue

                topic = msg.topic()
                logger.info(f"KAFKA DB CHANGE: topic={topic} offset={msg.offset()}")
                tools = TOPIC_TO_TOOLS.get(topic, []) if topic else []
                if tools:
                    with lock:
                        pending.update(tools)
                        last_event_time[0] = time.monotonic()
            except Exception as e:
                logger.error(f"KAFKA CONSUMER ERROR: {e}")

    threading.Thread(target=consume, daemon=True).start()
    threading.Thread(target=debounce_flush, daemon=True).start()