import os
import redis

from src.settings import (
    REDIS_HOST,
    REDIS_PORT,
    REDIS_DB
)


REDIS_URL = os.getenv("REDIS_URL")


if REDIS_URL:

    redis_client = redis.from_url(
        REDIS_URL,
        decode_responses=True
    )

else:

    redis_client = redis.Redis(
        host=REDIS_HOST,
        port=REDIS_PORT,
        db=REDIS_DB,
        decode_responses=True
    )


def check_redis_connection():
    return redis_client.ping()
def check_redis_connection():
    return redis_client.ping()