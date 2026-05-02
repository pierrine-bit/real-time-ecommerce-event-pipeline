# User Guide – Real-Time Data Pipeline

## Overview

This guide explains how to run, monitor, and validate the real-time data pipeline.

## Prerequisites

Install:

* Python 3.12+
* Apache Spark 3.5+
* Java 21+
* PostgreSQL 14+

Install dependencies:

```bash
pip install -r requirements.txt
```

## Environment Setup

Navigate to project:

```bash
cd ~/real_time_ecommerce_analytics
```

Activate environment:

```bash
source .venv/bin/activate
```

## PostgreSQL Setup

Start PostgreSQL:

```bash
sudo service postgresql start
```

Run setup:

```bash
psql -U postgres -f sql/postgres_setup.sql
```

## Running the Pipeline

Use two terminals.

### Terminal 1

```bash
python data_generator.py
```

### Terminal 2

```bash
spark-submit \
--packages org.postgresql:postgresql:42.7.3 \
spark_streaming_to_postgres.py
```

## Verify Results

Connect:

```bash
psql -h localhost -U postgres -d events_db
```

Check records:

```sql
SELECT COUNT(*)
FROM fact_events;
```

## Fault Recovery

Checkpoint directory prevents duplicate processing.

If needed:

```bash
rm -rf checkpoint/
mkdir checkpoint
```

Restart Spark.

## Troubleshooting

### Spark not processing

Verify:

* CSV files exist
* Spark is running
* Check logs

### PostgreSQL issues

Verify:

* Database is running
* Credentials in `.env`

## Conclusion

The pipeline continuously generates, processes, validates, and stores streaming event data.
