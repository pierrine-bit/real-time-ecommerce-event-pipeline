import logging


def write_to_postgres(
    batch_df,
    batch_id,
    db_url,
    db_properties,
    table_name
):
    """Persist micro-batch to PostgreSQL."""

    if batch_df.isEmpty():

        return

    try:

        (

            batch_df.write

            .mode(
                "append"
            )

            .jdbc(

                url=db_url,

                table=table_name,

                properties=db_properties

            )

        )

        logging.info(
            f"Batch {batch_id} loaded"
        )

    except Exception as error:

        logging.error(
            f"Batch {batch_id}: {error}"
        )

        raise
