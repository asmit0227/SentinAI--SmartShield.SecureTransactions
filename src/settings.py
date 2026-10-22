import os
from pathlib import Path

from dotenv import load_dotenv


BASE_DIR = Path(__file__).resolve().parent.parent

load_dotenv(BASE_DIR / ".env",override=True)


KAFKA_BOOTSTRAP_SERVERS = os.getenv("KAFKA_BOOTSTRAP_SERVER","localhost:9092")

REDIS_HOST = os.getenv("REDIS_HOST","localhost")

REDIS_PORT = int(os.getenv("REDIS_PORT", "6379"))

REDIS_DB = int(os.getenv("REDIS_DB", "0"))