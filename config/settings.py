import os

from dotenv import load_dotenv


load_dotenv()


APP_NAME = "RealTimeEcommerceAnalytics"

STREAM_INPUT_PATH = os.getenv("STREAM_INPUT_PATH", "stream_data")

CHECKPOINT_PATH = os.getenv("CHECKPOINT_PATH", "checkpoint")

POSTGRES_HOST = os.getenv("POSTGRES_HOST", "localhost")

POSTGRES_PORT = os.getenv("POSTGRES_PORT", "5432")

POSTGRES_DB = os.getenv("POSTGRES_DB", "events_db")

POSTGRES_USER = os.getenv("POSTGRES_USER", "postgres")

POSTGRES_PASSWORD = os.getenv("POSTGRES_PASSWORD", "securepassword")

POSTGRES_TABLE = os.getenv("POSTGRES_TABLE", "fact_events")

TRIGGER_INTERVAL = os.getenv("TRIGGER_INTERVAL", "10 seconds")

GENERATOR_OUTPUT_DIR = os.getenv("GENERATOR_OUTPUT_DIR", "stream_data")

GENERATOR_TMP_DIR = os.getenv("GENERATOR_TMP_DIR", "stream_data/tmp")

EVENTS_PER_FILE = int(os.getenv("EVENTS_PER_FILE", "1000"))

GENERATOR_SLEEP_TIME = int(os.getenv("GENERATOR_SLEEP_TIME", "3"))

ARCHIVE_DIR = os.getenv("ARCHIVE_DIR", "stream_data/archive")


DB_URL = (
    f"jdbc:postgresql://"
    f"{POSTGRES_HOST}:"
    f"{POSTGRES_PORT}/"
    f"{POSTGRES_DB}"
)


DB_PROPERTIES = {
    "user": POSTGRES_USER,
    "password": POSTGRES_PASSWORD,
    "driver": "org.postgresql.Driver"
}