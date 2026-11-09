import os
from pathlib import Path

from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.engine import URL
from sqlalchemy.orm import sessionmaker, declarative_base



BASE_DIR = Path(__file__).resolve().parent.parent


ENV_PATH = BASE_DIR / ".env"


load_dotenv(dotenv_path=ENV_PATH, override=True)



DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_HOST = os.getenv("DB_HOST")
DB_PORT = os.getenv("DB_PORT", "5432")
DB_NAME = os.getenv("DB_NAME")

DATABASE_URL = os.getenv("DATABASE_URL")


if DATABASE_URL:

    engine = create_engine(DATABASE_URL)

else:

    if not all([
        DB_USER,
        DB_PASSWORD,
        DB_HOST,
        DB_NAME
    ]):
        raise RuntimeError(
            "Database environment variables are missing."
        )

    local_database_url = URL.create(
        drivername="postgresql+psycopg2",
        username=DB_USER,
        password=DB_PASSWORD,
        host=DB_HOST,
        port=int(DB_PORT),
        database=DB_NAME
    )

    engine = create_engine(local_database_url)



SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)


Base = declarative_base()


def get_db():
    db = SessionLocal()

    try:
        yield db
    finally:
        db.close()