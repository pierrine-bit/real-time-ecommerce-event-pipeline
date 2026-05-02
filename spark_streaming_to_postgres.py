import logging

from pyspark.sql import SparkSession

from config.settings import (
    APP_NAME,
    STREAM_INPUT_PATH,
    CHECKPOINT_PATH,
    DB_URL,
    DB_PROPERTIES
)

from schemas.event_schema import event_schema
from streaming.reader import read_event_stream
from streaming.transformations import clean_events
from streaming.writer import write_to_postgres


logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s"
)


def create_spark_session():
    """Create Spark session."""

    return (
        SparkSession.builder
        .appName(APP_NAME)
        .config("spark.sql.shuffle.partitions", "2")
        .getOrCreate()
    )


def run_pipeline():
    """Start streaming pipeline."""

    try:

        spark = create_spark_session()

        spark.sparkContext.setLogLevel(
            "WARN"
        )

        raw_df = read_event_stream(
            spark,
            event_schema,
            STREAM_INPUT_PATH
        )

        clean_df = clean_events(
            raw_df
        )

        query = (

            clean_df
            .writeStream

            .foreachBatch(

                lambda df, batch_id:

                write_to_postgres(

                    df,

                    batch_id,

                    DB_URL,

                    DB_PROPERTIES,

                    "fact_events"

                )

            )

            .outputMode(
                "append"
            )

            .option(

                "checkpointLocation",

                CHECKPOINT_PATH

            )

            .start()

        )

        logging.info(
            "Pipeline started"
        )

        query.awaitTermination()

    except Exception as error:

        logging.error(
            f"Pipeline failed: {error}"
        )

        raise


if __name__ == "__main__":

    run_pipeline()
