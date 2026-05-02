import os
import csv
import time
import random
import logging

from faker import Faker

from datetime import (
    datetime,
    timedelta,
    UTC
)

from config.settings import (
    GENERATOR_OUTPUT_DIR as OUTPUT_DIR,
    GENERATOR_TMP_DIR as TMP_DIR,
    EVENTS_PER_FILE,
    GENERATOR_SLEEP_TIME as SLEEP_TIME
)


# =========================
# LOGGING CONFIGURATION
# =========================
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s"
)


os.makedirs(OUTPUT_DIR, exist_ok=True)
os.makedirs(TMP_DIR, exist_ok=True)

fake = Faker()
current_time = datetime.now(UTC)


# =========================
# STATIC REFERENCE DATA
# =========================
PRODUCTS = [
    (101, "Laptop", "Electronics", 1200),
    (102, "Phone", "Electronics", 800),
    (103, "Keyboard", "Accessories", 70),
    (104, "Mouse", "Accessories", 40)
]

COUNTRIES = [
    "Rwanda",
    "Kenya",
    "Ghana",
    "Nigeria"
]

DEVICES = [
    "mobile",
    "desktop"
]

SOURCES = [
    "facebook",
    "google",
    "organic"
]


def generate_user():
    """Generate user id with realistic distribution skew."""

    if random.random() < 0.3:
        return random.randint(1, 1000)

    return random.randint(1, 1_000_000)


# =========================
# EVENT GENERATION
# =========================
def generate_event():

    global current_time

    current_time += timedelta(seconds=1)

    product = random.choice(PRODUCTS)

    event_timestamp = current_time.replace(
        tzinfo=None
    ).strftime("%Y-%m-%d %H:%M:%S")

    return {
        "event_id": fake.uuid4(),
        "session_id": fake.uuid4(),
        "user_id": generate_user(),
        "event_type": random.choice(["view", "purchase"]),
        "product_id": product[0],
        "product_name": product[1],
        "category": product[2],
        "country": random.choice(COUNTRIES),
        "device_type": random.choice(DEVICES),
        "traffic_source": random.choice(SOURCES),
        "quantity": random.randint(1, 5),
        "price": product[3],
        "discount": round(random.uniform(0, 0.2), 2),
        "event_timestamp": event_timestamp
    }


# =========================
# CSV FILE WRITER
# =========================
def write_csv(index):

    try:

        final_path = os.path.join(
            OUTPUT_DIR,
            f"events_{index}.csv"
        )

        tmp_path = os.path.join(
            TMP_DIR,
            f"events_{index}.tmp"
        )

        sample_event = generate_event()

        with open(tmp_path, "w", newline="") as file:

            writer = csv.DictWriter(
                file,
                fieldnames=sample_event.keys()
            )

            writer.writeheader()
            writer.writerow(sample_event)

            for _ in range(EVENTS_PER_FILE - 1):
                writer.writerow(generate_event())

        os.replace(tmp_path, final_path)

        logging.info(f"Generated {final_path}")

    except Exception as error:

        logging.error(f"Generator failed: {error}")
        raise


def run_generator():

    index = 0

    try:

        while True:

            write_csv(index)

            index += 1

            time.sleep(SLEEP_TIME)

    except KeyboardInterrupt:

        logging.info("Generator stopped gracefully")


if __name__ == "__main__":
    run_generator()