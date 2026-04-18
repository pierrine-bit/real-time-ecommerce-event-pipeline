import logging
from pyspark.sql import SparkSession
from pyspark.sql.functions import col, hour, to_timestamp
from pyspark.sql.types import *

# =========================
# LOGGING CONFIG
# =========================
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s"
)

# =========================
# DATABASE CONFIG
# =========================
DB_URL = "jdbc:postgresql://localhost:5432/events_db"

DB_PROPERTIES = {
    "user": "postgres",
    "password": "postgres",
    "driver": "org.postgresql.Driver"
}

# =========================
# SPARK SESSION
# =========================
spark = SparkSession.builder \
    .appName("RealTimeEcommercePipeline") \
    .config("spark.sql.shuffle.partitions", "2") \
    .getOrCreate()

spark.sparkContext.setLogLevel("WARN")

# =========================
# SCHEMA
# =========================
schema = StructType([
    StructField("event_id", StringType(), True),
    StructField("user_id", IntegerType(), True),
    StructField("event_type", StringType(), True),
    StructField("product_id", IntegerType(), True),
    StructField("product_name", StringType(), True),
    StructField("price", DoubleType(), True),
    StructField("event_timestamp", StringType(), True)
])

# =========================
# READ STREAM
# =========================
df = spark.readStream \
    .schema(schema) \
    .option("header", "true") \
    .option("maxFilesPerTrigger", 1) \
    .csv("stream_data")

# =========================
# TRANSFORMATIONS
# =========================
clean_df = df \
    .withColumn("event_timestamp", to_timestamp(col("event_timestamp"))) \
    .withColumn("event_hour", hour(col("event_timestamp"))) \
    .filter(col("event_type").isin("view", "purchase")) \
    .filter(col("price") > 0) \
    .filter(col("event_id").isNotNull()) \
    .filter(col("event_timestamp").isNotNull()) \
    .dropDuplicates(["event_id"])

# =========================
# WRITE FUNCTION
# =========================
def write_to_postgres(batch_df, batch_id):
    """Write micro-batch to PostgreSQL."""
    if batch_df.isEmpty():
        return

    try:
        batch_df.write \
            .mode("append") \
            .jdbc(
                url=DB_URL,
                table="user_events",
                properties=DB_PROPERTIES
            )

        logging.info(f"Batch {batch_id} written successfully")

    except Exception as e:
        logging.error(f"Error in batch {batch_id}: {e}")

# =========================
# START STREAM
# =========================
query = clean_df.writeStream \
    .foreachBatch(write_to_postgres) \
    .outputMode("append") \
    .option("checkpointLocation", "checkpoint/") \
    .start()

query.awaitTermination()