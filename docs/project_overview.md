# Real-Time E-Commerce Analytics Pipeline

## Overview

This project builds a real-time data pipeline using Apache Spark Structured Streaming and PostgreSQL.

The pipeline simulates an e-commerce platform where customer activities such as product views and purchases are continuously generated, processed as they arrive, and stored for analytical use.

## Objectives

The project focuses on:

* Generating continuous event data
* Processing streaming data in real time
* Validating incoming records
* Enriching event data
* Preventing duplicate processing
* Recovering safely after failure
* Measuring system performance

## Technology Stack

* Python (`Faker`)
* Apache Spark Structured Streaming
* PostgreSQL
* JDBC

## Project Structure

```text
real_time_ecommerce_analytics/
├── config/
├── schemas/
├── streaming/
├── sql/
├── docs/
├── stream_data/
├── checkpoint/
├── data_generator.py
├── main.py
├── spark_streaming_to_postgres.py
├── postgres_connection_details.txt
├── .env
├── requirements.txt
└── README.md
```

## Pipeline Description

### Data Generation

The generator creates synthetic e-commerce events and writes them as CSV files.

### Streaming and Processing

Spark monitors the input directory and performs:

* Schema enforcement
* Timestamp conversion
* Event hour extraction
* Revenue calculation
* Invalid record filtering
* Duplicate removal
* Checkpoint recovery

### Data Storage

Database: `events_db`

Table: `fact_events`

## Data Flow

```text
Data Generator
      ↓
CSV Event Files
      ↓
Spark Structured Streaming
      ↓
Validation + Enrichment
      ↓
PostgreSQL
      ↓
Business Analytics
```

Architecture diagram:

`docs/system_architecture.png`

## Conclusion

The pipeline processes streaming events continuously with reliable storage, fault recovery, and stable execution.
