
# Test Cases – Real-Time Data Pipeline

## 1. Overview

This document defines validation scenarios for the real-time data ingestion pipeline built using:

* Python (data generation)
* Spark Structured Streaming
* PostgreSQL (storage)

The goal is to verify correctness, reliability, fault tolerance, and performance under continuous streaming conditions.

---

## 2. Test Environment

* OS: Ubuntu (WSL)
* Python: 3.12.x
* Spark: 3.5.x (local mode)
* PostgreSQL: 14+
* Input Source: CSV files (`stream_data/`)

---

## 3. Test Cases

---

### Test Case 1: Streaming Data Generation

**Objective:**
Verify that the generator produces continuous, high-volume event data.

**Procedure:**

1. Run `data_generator.py`
2. Monitor `stream_data/` directory
3. Inspect generated files

**Expected Result:**

* Files are generated every few seconds
* Each file contains around 1000 records
* Schema matches the expected format

**Actual Result:**
As expected

**Validation (Shell):**

```bash
head stream_data/events_0.csv
```

---

### Test Case 2: Stream Ingestion Detection

**Objective:**
Verify that Spark detects and processes new files automatically.

**Procedure:**

1. Start the Spark streaming job
2. Start the data generator
3. Observe Spark logs and Spark UI (`localhost:4040`)

**Expected Result:**

* Micro-batches are triggered automatically
* No manual intervention is required
* No ingestion errors occur

**Actual Result:**
As expected

**Validation Indicator:**

```text
Batch X written successfully
```

---

### Test Case 3: Data Transformation Accuracy

**Objective:**
Verify that data transformations are applied correctly.

**Procedure:**

1. Allow the pipeline to run
2. Query PostgreSQL

**Validation Query:**

```sql
SELECT event_type, event_hour, event_timestamp
FROM user_events
LIMIT 10;
```

**Expected Result:**

* `event_hour` matches the timestamp
* `event_timestamp` is correctly parsed
* Only valid event types exist

**Actual Result:**
As expected

---

### Test Case 4: Data Persistence

**Objective:**
Verify that data is stored correctly in PostgreSQL.

**Procedure:**

1. Connect to the database
2. Execute:

```sql
SELECT COUNT(*) FROM user_events;
```

**Expected Result:**

* Record count increases continuously
* No write failures occur

**Actual Result:**
As expected

---

### Test Case 5: Idempotency / Deduplication

**Objective:**
Verify that duplicate events are not stored.

**Procedure:**

1. Restart the Spark job
2. Run the validation query

**Validation Query:**

```sql
SELECT event_id, COUNT(*)
FROM user_events
GROUP BY event_id
HAVING COUNT(*) > 1;
```

**Expected Result:**

* No duplicate records are returned

**Actual Result:**
As expected

---

### Test Case 6: Fault Tolerance (Checkpoint Recovery)

**Objective:**
Verify recovery using checkpointing.

**Procedure:**

1. Stop the Spark job
2. Generate additional data
3. Restart the Spark job

**Expected Result:**

* Previously processed data is not reprocessed
* New data is processed correctly
* No duplicate insertion occurs

**Actual Result:**
As expected

---

### Test Case 7: Performance Stability

**Objective:**
Assess system behavior under continuous load.

**Procedure:**

1. Run the generator for 3–5 minutes
2. Monitor Spark UI (`localhost:4040`)

**Expected Result:**

* Stable batch execution times (~150–400 ms)
* No memory or executor failures
* Continuous ingestion without backlog

**Actual Result:**
As expected

---

### Test Case 8: Data Validation Enforcement

**Objective:**
Verify that invalid data is filtered out.

**Procedure:**

1. Query the database
2. Run validation queries

**Validation Queries:**

```sql
SELECT * FROM user_events
WHERE event_type NOT IN ('view','purchase');

SELECT * FROM user_events
WHERE price <= 0;
```

**Expected Result:**

* No invalid event types are present
* No records with non-positive price

**Actual Result:**
As expected

---

## 4. Test Summary

The test results confirm that the pipeline:

* Processes streaming data correctly
* Applies transformations as expected
* Maintains data integrity (no duplicates)
* Enforces validation rules
* Recovers from failures using checkpointing
* Remains stable under continuous load

---

## 5. Conclusion

The pipeline operates reliably under real-time conditions.
It successfully handles data ingestion, transformation, and storage, and is able to recover from failures without data loss or duplication.
