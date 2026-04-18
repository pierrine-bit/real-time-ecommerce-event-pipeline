import os
import time
import csv
import random
import logging
from datetime import datetime, timedelta
from faker import Faker

# =========================
# LOGGING CONFIG
# =========================
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s"
)

# =========================
# CONFIGURATION
# =========================
OUTPUT_DIR = "stream_data"
TMP_DIR = "stream_data/tmp"

EVENTS_PER_FILE = 1000
SLEEP_TIME = 3

os.makedirs(OUTPUT_DIR, exist_ok=True)
os.makedirs(TMP_DIR, exist_ok=True)

fake = Faker()

EVENT_TYPES = ["view", "purchase"]

PRODUCTS = [
    (101, "Laptop", 1200.50),
    (102, "Phone", 800.00),
    (103, "Headphones", 150.75),
    (104, "Keyboard", 70.20),
    (105, "Mouse", 40.99)
]

current_time = datetime.utcnow()


def generate_user():
    """Generate user_id with skewed distribution."""
    if random.random() < 0.3:
        return random.randint(1, 1000)
    return random.randint(1, 1_000_000)


def generate_event():
    """Generate one event with sequential timestamp."""
    global current_time
    current_time += timedelta(seconds=1)

    product = random.choice(PRODUCTS)

    return {
        "event_id": fake.uuid4(),
        "user_id": generate_user(),
        "event_type": random.choice(EVENT_TYPES),
        "product_id": product[0],
        "product_name": product[1],
        "price": round(product[2] * random.uniform(0.9, 1.1), 2),
        "event_timestamp": current_time.strftime("%Y-%m-%d %H:%M:%S")
    }


def write_csv(index):
    """Write events safely using atomic file creation."""
    try:
        final_path = os.path.join(OUTPUT_DIR, f"events_{index}.csv")
        tmp_path = os.path.join(TMP_DIR, f"events_{index}.csv.tmp")

        with open(tmp_path, "w", newline="") as f:
            writer = csv.DictWriter(
                f,
                fieldnames=[
                    "event_id",
                    "user_id",
                    "event_type",
                    "product_id",
                    "product_name",
                    "price",
                    "event_timestamp"
                ]
            )
            writer.writeheader()

            for _ in range(EVENTS_PER_FILE):
                writer.writerow(generate_event())

        os.rename(tmp_path, final_path)
        logging.info(f"Generated {final_path}")

    except Exception as e:
        logging.error(f"Error writing file {index}: {e}")


if __name__ == "__main__":
    idx = 0
    logging.info("Starting data generator...")

    while True:
        write_csv(idx)
        idx += 1
        time.sleep(SLEEP_TIME)