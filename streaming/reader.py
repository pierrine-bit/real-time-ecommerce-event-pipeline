def read_event_stream(
    spark,
    schema,
    input_path
):
    """Read streaming events."""

    return (

        spark.readStream

        .schema(schema)

        .option(
            "header",
            "true"
        )

        .option(
            "maxFilesPerTrigger",
            1
        )

        .csv(
            input_path
        )

    )
