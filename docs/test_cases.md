
# Test Cases — Real-Time E-Commerce Analytics Pipeline

## 1. Purpose

This document records the validation performed to verify the correctness, reliability, and stability of the real-time e-commerce analytics pipeline.

Validation covered:

* event generation
* stream ingestion
* transformation
* PostgreSQL loading
* duplicate prevention
* checkpoint recovery
* runtime stability

# 2. Test Environment

| Component        |            Specification |
| ---------------- | -----------------------: |
| Operating System |               Ubuntu WSL |
| Python           |                     3.12 |
| Apache Spark     |                    4.1.1 |
| Java             |                       21 |
| Database         |            PostgreSQL 16 |
| Input Source     |                CSV files |
| Output Sink      | PostgreSQL `fact_events` |

# 3. Test Cases

## Test Case 1 — Event Generation

### Validation

```bash
python data_generator.py
```

### Result

CSV files were generated continuously in `stream_data/`.

Example:

```text
Generated stream_data/events_0.csv
Generated stream_data/events_1.csv
Generated stream_data/events_2.csv
```

**Status:** PASS


## Test Case 2 — Stream Ingestion

### Validation

```bash
spark-submit \
--packages org.postgresql:postgresql:42.7.3 \
spark_streaming_to_postgres.py
```

### Result

Spark started successfully and processed files continuously.

Example:

```text
Pipeline started
Batch 32 loaded
Batch 33 loaded
Batch 34 loaded
```

**Status:** PASS

## Test Case 3 — PostgreSQL Table Validation

### Validation

```sql
\dt
```

### Result

```text
fact_events
user_events
```

Both tables were available.

**Status:** PASS

## Test Case 4 — Data Load Validation

### Validation

```sql
SELECT COUNT(*) FROM fact_events;
```

### Result

Record count increased during execution.

Example:

```text
42,000
54,000
78,000+
```

**Status:** PASS

## Test Case 5 — Duplicate Validation

### Validation

```sql
SELECT event_id, COUNT(*)
FROM fact_events
GROUP BY event_id
HAVING COUNT(*) > 1;
```

### Result

```text
0 rows
```

No duplicate records detected.

**Status:** PASS

## Test Case 6 — Event Type Validation

### Validation

```sql
SELECT COUNT(*)
FROM fact_events
WHERE event_type NOT IN ('view', 'purchase');
```

### Result

```text
0
```

**Status:** PASS

---

## Test Case 7 — Price Validation

### Validation

```sql
SELECT COUNT(*)
FROM fact_events
WHERE price <= 0;
```

### Result

```text
0
```

**Status:** PASS

## Test Case 8 — Quantity Validation

### Validation

```sql
SELECT COUNT(*)
FROM fact_events
WHERE quantity <= 0;
```

### Result

```text
0
```

**Status:** PASS

## Test Case 9 — Null Event ID Validation

### Validation

```sql
SELECT COUNT(*)
FROM fact_events
WHERE event_id IS NULL;
```

### Result

```text
0
```

**Status:** PASS

## Test Case 10 — Checkpoint Recovery

### Validation

After restarting Spark with the existing checkpoint directory:

```sql
SELECT event_id, COUNT(*)
FROM fact_events
GROUP BY event_id
HAVING COUNT(*) > 1;
```

### Result

```text
0 rows
```

Previously processed files were not reloaded.

**Status:** PASS

## Test Case 11 — Runtime Stability

### Result

Pipeline remained stable during continuous execution.

Observed logs:

```text
Batch 45 loaded
Batch 46 loaded
Batch 47 loaded
Batch 48 loaded
```

No failures occurred during processing.

**Status:** PASS

# 4. Validation Summary

| Validation Area       | Status |
| --------------------- | -----: |
| Event generation      |   PASS |
| Stream ingestion      |   PASS |
| PostgreSQL loading    |   PASS |
| Duplicate prevention  |   PASS |
| Event type validation |   PASS |
| Price validation      |   PASS |
| Quantity validation   |   PASS |
| Null validation       |   PASS |
| Checkpoint recovery   |   PASS |
| Runtime stability     |   PASS |

# 5. Conclusion

The pipeline was successfully validated end-to-end.

