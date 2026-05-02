from pyspark.sql.functions import (
    col,
    hour,
    to_timestamp
)


def clean_events(df):
    """Validate, enrich, and deduplicate events."""

    return (

        df

        .withColumn(
            "event_id",
            col("event_id").cast("string")
        )

        .withColumn(
            "session_id",
            col("session_id").cast("string")
        )

        .withColumn(

            "event_timestamp",

            to_timestamp(
                col("event_timestamp")
            )

        )

        .withColumn(

            "event_hour",

            hour(
                col("event_timestamp")
            )

        )

        .withColumn(

            "revenue",

            col("quantity")
            *
            col("price")
            *
            (
                1 -
                col("discount")
            )

        )

        .filter(
            col("event_type")
            .isin(
                "view",
                "purchase"
            )
        )

        .filter(
            col("price") > 0
        )

        .filter(
            col("quantity") > 0
        )

        .filter(
            col("event_id")
            .isNotNull()
        )

        .dropDuplicates(
            ["event_id"]
        )

    )
