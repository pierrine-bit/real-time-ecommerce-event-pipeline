

# Real-Time E-Commerce Events Pipeline

## Project Overview

This project builds a real-time data pipeline using **Apache Spark Structured Streaming** and **PostgreSQL**.
It simulates an e-commerce system where user activities, such as viewing or purchasing products, are generated continuously, processed as they arrive, and stored for later use.

The main goal is to handle streaming data in a reliable and efficient way.

---

## Objectives

* Generate continuous event data using Python
* Process data in real time using Spark
* Clean and validate incoming data
* Store processed data in PostgreSQL
* Make the system reliable using checkpointing
* Observe how the system performs under continuous load

---

## Key Features

* Real-time processing using Spark micro-batches
* High-volume event generation (~1000 events per file)
* Sequential timestamps to mimic real-time data
* Data validation (removing invalid records)
* Deduplication using a unique `event_id`
* Fault tolerance using checkpointing
* Efficient data writing to PostgreSQL

---

## Technology Stack

* Python (Faker)
* Apache Spark Structured Streaming
* PostgreSQL
* JDBC

---

## Project Structure

```text id="simple1"
project/
│
├── data_generator.py
├── spark_streaming_to_postgres.py
├── postgres_setup.sql
├── postgres_connection_details.txt
├── project_overview.md
├── test_cases.md
├── performance_metrics.md
├── user_guide.md
│
├── stream_data/      # Input data directory
├── checkpoint/       # Spark checkpoint directory
```

---

## Pipeline Description

### Data Generation

A Python script generates fake e-commerce events and writes them as CSV files.
Each event includes user details, product information, price, and a timestamp.

Files are written safely by first creating a temporary file and then renaming it.

---

### Streaming and Processing

Spark monitors the input folder and processes new files in small batches.

During processing, the system:

* Applies a fixed schema
* Converts timestamps and extracts useful fields
* Filters invalid data
* Removes duplicate records using `event_id`
* Writes the cleaned data to PostgreSQL
* Uses checkpointing to recover from failures

---

### Data Storage

Processed data is stored in PostgreSQL:

* Database: `events_db`
* Table: `user_events`
* `event_id` is used to prevent duplicate records

---

## Data Flow

```text id="simple2"
Data Generator → CSV Files → Spark → Processing → PostgreSQL
```

---

## Execution and Testing

Steps for running the project are provided in `user_guide.md`.
Testing and validation details are available in `test_cases.md`.

---

## Key Points

* The system avoids duplicate data using unique IDs
* Checkpointing allows recovery after failure
* Data is validated before being stored
* The pipeline handles continuous data smoothly

---

## Conclusion

This project shows how a real-time data pipeline can be built using simple tools.
It demonstrates important concepts such as streaming, data validation, and fault tolerance in a practical way.
