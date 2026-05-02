
# Performance Metrics – Real-Time Data Pipeline

## 1. Overview

This document evaluates the performance of the real-time data ingestion pipeline built using:

* Python (data generation)
* Spark Structured Streaming
* PostgreSQL (JDBC sink)

The objective is to assess latency, throughput, and system stability under continuous streaming load.

---

## 2. Test Configuration

* Execution Mode: Spark Local Mode
* Input Source: CSV files (`stream_data/`)
* Processing Model: Micro-batch streaming
* Events per File: ~1000
* Files per Batch: 1
* Approximate Input Rate: ~300-400 events/second

---

## 3. Metrics Collected

---

### 3.1 Latency

**Definition:**
Time elapsed between event generation and insertion into PostgreSQL.

**Measurement Method:**

Latency was approximated using Spark micro-batch processing time observed in the Spark UI and driver logs.

**Observed Result:**

```text
Average Latency: ~0.5 – 1 second
````

**Analysis:**

* Low latency achieved due to small micro-batches
* Suitable for near real-time processing

---

### 3.2 Throughput

**Definition:**
Number of events processed per second.

**Measurement:**

```text
Input rate: ~300-400 events/sec  
Observed throughput: matched input rate with no backlog
```

**Analysis:**

* Spark sustained ingestion rate without delay
* No accumulation of unprocessed data

---

### 3.3 Micro-Batch Processing Time

**Definition:**
Time taken to process each micro-batch.

**Measurement Tool:**

* Spark UI (`http://localhost:4040`)

**Observed Result:**

```text
Batch Duration: ~150 – 400 ms
```

**Analysis:**

* Batch duration remained consistent with low variance
* Processing time is lower than ingestion interval
* Confirms stable execution without delays

---

### 3.4 System Stability

**Observation Period:**
5+ minutes continuous execution

**Observed Result:**

* No crashes
* No memory errors
* Continuous database writes

**Analysis:**

* System maintains processing capacity greater than ingestion rate
* No backlog observed under sustained load

---

### 3.5 Resource Utilization

**Observation Tool:**
Spark UI and system monitor

**Observed Results:**

```text
CPU Usage: ~25–40%  
Memory Usage: ~400–600 MB
```

**Analysis:**

* Resource usage remained stable throughout execution
* No memory spikes or executor failures observed
* Indicates available capacity for scaling
Measurements were taken in a local WSL environment and may vary depending on hardware configuration.
---

### 3.6 Metric Relationship Analysis

* Throughput (~300-400 events/sec) matches input rate
* Batch duration (150–400 ms) is lower than ingestion interval
* Processing keeps up with data arrival

**Result:**

* No backlog
* Stable processing
* System operating efficiently

---

## 4. Bottleneck Analysis

### Identified Bottlenecks:

1. **JDBC Writes (PostgreSQL)**

JDBC writes introduce higher latency compared to in-memory Spark operations and may become a bottleneck as data volume increases.

2. **Single-node Execution**

   * Local mode limits parallel processing capability

3. **File-based Streaming Source**

Less efficient compared to distributed streaming platforms such as Kafka.

---

## 5. Optimizations Applied

* Explicit schema to avoid inference overhead
* Early filtering to reduce data volume
* `foreachBatch` for efficient JDBC writes
* Checkpointing for fault tolerance
* Deduplication using `event_id`

---

## 6. Recommended Improvements

To scale this system further:

* Replace CSV ingestion with Kafka
* Use connection pooling for PostgreSQL
* Partition data for parallel execution
* Deploy Spark in cluster mode

---

## 7. Conclusion

The pipeline demonstrates:

* Low latency (~1 second)
* High throughput (~300-400 events/sec)
* Stable performance under continuous load

The system efficiently processes streaming data in a local environment and reflects production-level design principles. With additional infrastructure, it can scale to handle larger, real-world workloads.

