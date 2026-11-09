import os
from pathlib import Path

from dotenv import load_dotenv


BASE_DIR = Path(__file__).resolve().parent.parent

load_dotenv(BASE_DIR / ".env",override=True)


KAFKA_BOOTSTRAP_SERVERS = os.getenv(
    "KAFKA_BOOTSTRAP_SERVER",
    "localhost:9092")

KAFKA_SECURITY_PROTOCOL = os.getenv(
    "KAFKA_SECURITY_PROTOCOL",
    "PLAINTEXT"
)

KAFKA_SASL_MECHANISM = os.getenv(
    "KAFKA_SASL_MECHANISM"
)

KAFKA_SASL_USERNAME = os.getenv(
    "KAFKA_SASL_USERNAME"
)

KAFKA_SASL_PASSWORD = os.getenv(
    "KAFKA_SASL_PASSWORD"
)

REDIS_HOST = os.getenv("REDIS_HOST","localhost")

REDIS_PORT = int(os.getenv("REDIS_PORT", "6379"))

REDIS_DB = int(os.getenv("REDIS_DB", "0"))

def get_kafka_config():

    config = {
        "bootstrap.servers": KAFKA_BOOTSTRAP_SERVERS
    }

    if KAFKA_SECURITY_PROTOCOL != "PLAINTEXT":

        config.update({
            "security.protocol": KAFKA_SECURITY_PROTOCOL,
            "sasl.mechanism": KAFKA_SASL_MECHANISM,
            "sasl.username": KAFKA_SASL_USERNAME,
            "sasl.password": KAFKA_SASL_PASSWORD
        })

    return config