
# Project Overview – Real-Time Data Ingestion Pipeline

## Objective

This project implements a real-time data pipeline that simulates an e-commerce platform capturing user activity such as product views and purchases. The system continuously generates event data, processes it using Apache Spark Structured Streaming, and stores it in a PostgreSQL database for downstream analysis.

---

## System Components

### 1. Data Generator

* Generates high-volume synthetic e-commerce events
* Writes data as CSV files into a monitored directory
* Produces sequential event streams using timestamp progression

---

### 2. Spark Structured Streaming

* Monitors the input directory for new files
* Applies schema enforcement and transformations
* Processes data in micro-batches
* Performs validation and deduplication using `event_id`
* Writes processed data to PostgreSQL
* Uses checkpointing for fault tolerance and recovery

---

### 3. PostgreSQL Database

* Stores processed event data
* Enforces constraints (e.g., unique `event_id`)
* Supports efficient querying through indexing

---

## Data Flow

```text
Data Generator → CSV Files → Spark Streaming → PostgreSQL
````

---

## Key Features

* Real-time data ingestion using micro-batch processing
* Schema validation and data transformation
* Fault tolerance through checkpointing
* Idempotent processing using `event_id` and database constraints
* Scalable pipeline design with performance optimizations

---

## Learning Outcomes

* Building real-time data pipelines
* Using Spark Structured Streaming for continuous processing
* Integrating streaming systems with relational databases
* Understanding fault tolerance and idempotency in streaming systems

---

## Conclusion

The project demonstrates a complete, end-to-end streaming pipeline with production-style design considerations. It provides a strong foundation for building scalable, real-world data engineering systems.
