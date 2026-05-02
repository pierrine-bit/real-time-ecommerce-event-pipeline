# Performance Metrics – Real-Time Data Pipeline

## Purpose

This document presents the performance evaluation of the real-time data pipeline.


## Test Environment

| Parameter | Value |
|-----------|--------|
| Operating System | Ubuntu (WSL) |
| Execution Mode | Spark Local Mode |
| Streaming Source | CSV files (`stream_data/`) |
| Processing Model | Micro-batch |
| Events per File | ~1000 |
| Files per Trigger | 1 |
| Input Rate | ~300–400 events/sec |
| Database | PostgreSQL |


## Performance Measurements

### Processing Latency

Observed result:

```text
Average Latency: ~0.5–1 second
```

Observation:

The pipeline maintained near real-time processing with no delayed batches.


### Throughput

Observed result:

```text
Input Rate: ~300–400 events/sec
Observed Throughput: matched input rate
```

Observation:

No processing backlog was observed.


### Micro-Batch Execution

Observed result:

```text
Batch Duration: ~150–400 ms
```

Observation:

Batch execution remained below the ingestion interval.


### System Stability

Observed result:

- No application failures
- No executor failures
- No memory issues
- Continuous database writes
- No duplicate records


### Resource Utilization

Observed result:

```text
CPU Usage: ~25–40%
Memory Usage: ~400–600 MB
```

Observation:

Resource utilization remained stable during execution.


## Bottlenecks Identified

### JDBC Database Writes

Database writes introduced higher latency than in-memory processing.

### Single-Node Execution

Local mode limits parallel processing.

### File-Based Streaming

CSV ingestion introduces file system overhead.


## Optimizations Applied

The pipeline uses:

- Explicit schema definition
- Early filtering
- Deduplication using `event_id`
- `foreachBatch` JDBC writes
- Checkpoint recovery
- Database indexing


## Scaling Opportunities

To support higher event volumes:

- Replace CSV ingestion with Kafka
- Run Spark in cluster mode
- Partition workloads across executors
- Use connection pooling
- Containerize deployment


## Conclusion

The pipeline processed continuous workloads with:

- Low latency
- Stable throughput
- Reliable fault recovery
- Stable resource utilization