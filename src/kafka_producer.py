import json

from confluent_kafka import Producer

from src.settings import KAFKA_BOOTSTRAP_SERVERS
from src.logger import get_logger


logger = get_logger(__name__)

TOPIC = "fraud-transactions"


producer = Producer({
    "bootstrap.servers": KAFKA_BOOTSTRAP_SERVERS
})


def send_transaction(transaction: dict):

    delivery_result = {
        "error": None
    }

    def delivery_report(err, msg):

        if err is not None:
            delivery_result["error"] = err
            return

        logger.info(
            f"Transaction delivered to Kafka | "
            f"topic={msg.topic()} "
            f"partition={msg.partition()} "
            f"offset={msg.offset()}"
        )

    transaction_id = transaction.get("transaction_id")

    producer.produce(
        TOPIC,
        key=str(transaction_id),
        value=json.dumps(transaction),
        callback=delivery_report
    )

    remaining_messages = producer.flush(timeout=5)

    if remaining_messages > 0:
        raise RuntimeError(
            f"Kafka delivery timed out. "
            f"{remaining_messages} message(s) still pending."
        )

    if delivery_result["error"] is not None:
        raise RuntimeError(
            f"Kafka delivery failed: {delivery_result['error']}"
        )

    return True