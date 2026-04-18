
# User Guide – Real-Time Data Ingestion Using Spark Structured Streaming & PostgreSQL
## 1. Overview

This guide explains how to run the real-time data pipeline that simulates e-commerce events, processes them using Apache Spark Structured Streaming, and stores the results in PostgreSQL.

The pipeline consists of:

* Data Generator → produces streaming CSV data
* Spark Streaming Job → processes data in real time
* PostgreSQL → stores processed events

---

## 2. Prerequisites

Ensure the following are installed:

* Python 3.14
* Apache Spark 3.5+
* Java 21+
* PostgreSQL 14+

### Install Python dependencies:

```bash
pip install faker
````

---

## 3. Project Structure

```text
project/
│
├── data_generator.py
├── spark_streaming_to_postgres.py
├── postgres_setup.sql
├── test_cases.md
├── user_guide.md
│
├── stream_data/       # input data directory
├── checkpoint/        # Spark checkpoint directory
```

---

## 4. PostgreSQL Setup

### Step 1: Start PostgreSQL

```bash
sudo service postgresql start
```

---

### Step 2: Create Database and Table

```bash
psql -U postgres -f postgres_setup.sql
```

---

## 5. Running the Pipeline

 You must use **two terminals**

---

### Terminal 1: Start Spark Streaming

```bash
spark-submit \
  --packages org.postgresql:postgresql:42.7.3 \
  spark_streaming_to_postgres.py
```

Expected output:

```text
Batch 0 written successfully
Batch 1 written successfully
```

---

### Terminal 2: Start Data Generator

```bash
python data_generator.py
```

Expected output:

```text
Generated stream_data/events_0.csv
Generated stream_data/events_1.csv
```

---

## 6. Verify Data

Connect to PostgreSQL:

```bash
psql -U postgres -d events_db
```

Run:

```sql
SELECT COUNT(*) FROM user_events;
```

```sql
SELECT * 
FROM user_events 
ORDER BY event_timestamp DESC 
LIMIT 10;
```

Expected:

* Row count increases continuously
* Data appears in real time

---

## 7. Fault Tolerance (Checkpointing)

The system uses a `checkpoint/` directory to:

* Track processed data
* Recover after failure
* Prevent duplicate processing

 If errors occur:

```bash
rm -rf checkpoint/
```

---

## 8. Stopping the Pipeline

Press:

```text
CTRL + C
```

in both terminals.

---

## 9. Troubleshooting

### Spark not processing data

* Ensure new CSV files are being generated
* Spark only processes new files

---

### PostgreSQL connection error

* Check username/password
* Ensure PostgreSQL is running

---

### Duplicate data issue

* Ensure checkpoint directory is not reused incorrectly
* Confirm `.dropDuplicates(["event_id"])` is applied
* Verify `event_id` is PRIMARY KEY in database

---

## 10. Notes

* Spark uses micro-batch processing
* CSV simulates streaming ingestion
* In production, Kafka would replace CSV input

---

## 11. Conclusion

This pipeline demonstrates:

* Real-time data ingestion
* Data transformation using Spark
* Reliable storage in PostgreSQL
* Fault-tolerant and idempotent streaming architecture

It reflects real-world data engineering practices and scalable design principles.
