# Real-Time E-Commerce Analytics

## Overview

This project delivers a real-time analytics pipeline for e-commerce event data using Apache Spark Structured Streaming and PostgreSQL.

The solution captures customer activities such as product views and purchases, processes incoming events in near real time, applies data quality controls and business transformations, and persists analytics-ready records for downstream reporting.

The architecture focuses on operational reliability, data integrity, fault recovery, and performance under continuous streaming workloads.

## Business Objectives

The pipeline addresses the following business and engineering objectives:

* Capture customer activity continuously
* Process streaming events in near real time
* Enforce data quality and validation rules
* Enrich raw events with business metrics
* Persist analytics-ready records
* Prevent duplicate processing
* Recover safely from failures
* Support operational and analytical reporting

## Core Capabilities

### Event Generation

A Python-based generator produces synthetic e-commerce events with sequential timestamps to simulate live customer activity.

### Streaming Processing

Apache Spark Structured Streaming processes incoming event files using micro-batch execution.

Processing includes:

* Schema enforcement
* Timestamp normalization
* Event enrichment
* Revenue calculation
* Invalid record filtering
* Duplicate detection

### Persistent Storage

Processed records are written to PostgreSQL using batch-based JDBC writes.

### Fault Recovery

Checkpointing preserves streaming state and supports restart recovery without data duplication.

### Business Analytics

The processed dataset supports analytical workloads including:

* Revenue analysis
* Product performance
* Conversion analysis
* Geographic performance
* Peak transaction periods

## Technology Stack

| Component            | Technology                        |
| -------------------- | --------------------------------- |
| Programming Language | Python                            |
| Data Generation      | Faker                             |
| Stream Processing    | Apache Spark Structured Streaming |
| Storage              | PostgreSQL                        |
| Connectivity         | JDBC                              |

## Solution Architecture

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

System architecture diagram:

`docs/system_architecture.png`

## Project Structure

```text
real_time_ecommerce_analytics/
├── config/
├── schemas/
├── streaming/
├── sql/
├── docs/
│   └── system_architecture.png
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

## Data Model

### Database

`events_db`

### Fact Table

`fact_events`

### Stored Attributes

* Event identifiers
* Session identifiers
* Product attributes
* Customer geography
* Device information
* Traffic source
* Quantity
* Price
* Discount
* Revenue
* Event timestamp
* Event hour

## Performance Summary

| Metric             | Result              |
| ------------------ | ------------------- |
| Processing Latency | ~0.5–1 second       |
| Throughput         | ~300–400 events/sec |
| Batch Duration     | ~150–400 ms         |
| Memory Usage       | ~400–600 MB         |
| CPU Usage          | ~25–40%             |

## Data Integrity Controls

The solution applies:

* Explicit schema validation
* Business rule enforcement
* Primary key constraints
* Event deduplication using `event_id`
* Indexed query optimization
* Checkpoint-based recovery

## Scalability Roadmap

Recommended next steps:

* Replace file-based ingestion with Kafka
* Deploy Spark in cluster mode
* Introduce connection pooling
* Containerize deployment
* Add workflow orchestration

## Conclusion

The solution processes continuous e-commerce event streams with low latency, stable throughput, reliable fault recovery, and consistent data quality.
