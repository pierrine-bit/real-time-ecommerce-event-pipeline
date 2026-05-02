# Test Cases – Real-Time Data Pipeline

## Purpose

This document defines the validation scenarios used to verify correctness, reliability, fault recovery, and operational stability.


## Test Environment

| Parameter | Value |
|-----------|--------|
| Operating System | Ubuntu (WSL) |
| Python Version | 3.12.x |
| Spark Version | 3.5.x |
| Execution Mode | Local Mode |
| Database | PostgreSQL 14+ |
| Input Source | CSV files (`stream_data/`) |


## Validation Scenarios

### Test Case 1: Streaming Data Generation

**Objective**

Verify continuous generation of event files.

**Validation**

```bash
head stream_data/events_0.csv
```

**Expected Result**

- Files are generated continuously
- Each file contains approximately 1000 records
- Generated files follow the expected schema

**Observed Result**

Passed.


### Test Case 2: Stream Ingestion Detection

**Objective**

Verify automatic ingestion of new files.

**Validation Indicator**

```text
Batch X loaded
```

**Expected Result**

- Micro-batches start automatically
- No ingestion failures occur

**Observed Result**

Passed.


### Test Case 3: Data Transformation Accuracy

**Objective**

Verify transformations.

**Validation Query**

```sql
SELECT event_type, event_hour, event_timestamp
FROM fact_events
LIMIT 10;
```

**Expected Result**

- Correct timestamps
- Correct event hours
- Valid event types

**Observed Result**

Passed.


### Test Case 4: Data Persistence

**Objective**

Verify data storage.

**Validation Query**

```sql
SELECT COUNT(*)
FROM fact_events;
```

**Expected Result**

Record count increases continuously.

**Observed Result**

Passed.


### Test Case 5: Deduplication

**Objective**

Verify duplicate prevention.

**Validation Query**

```sql
SELECT event_id, COUNT(*)
FROM fact_events
GROUP BY event_id
HAVING COUNT(*) > 1;
```

**Expected Result**

No duplicate records.

**Observed Result**

Passed.


### Test Case 6: Fault Recovery

**Objective**

Verify checkpoint recovery.

**Expected Result**

Previously processed data is not reprocessed.

**Observed Result**

Passed.


### Test Case 7: Performance Stability

**Objective**

Verify stable execution.

**Expected Result**

- Stable batch execution
- No memory failures
- No backlog

**Observed Result**

Passed.


### Test Case 8: Data Validation

**Objective**

Verify invalid records are filtered.

**Validation Queries**

```sql
SELECT *
FROM fact_events
WHERE event_type NOT IN ('view','purchase');
```

```sql
SELECT *
FROM fact_events
WHERE price <= 0;
```

**Expected Result**

No invalid records.

**Observed Result**

Passed.


## Conclusion

All validation scenarios completed successfully.