import os
import glob
import shutil
import logging


def write_to_postgres(
    batch_df,
    batch_id,
    db_url,
    db_properties,
    table_name,
    input_dir=None,
    archive_dir=None
):
    """Persist micro-batch to PostgreSQL then archive processed CSV files."""

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

    if input_dir and archive_dir:
        _archive_processed_files(input_dir, archive_dir, batch_id)


def _archive_processed_files(input_dir, archive_dir, batch_id):
    """Move processed CSV files from input_dir to archive_dir."""

    os.makedirs(archive_dir, exist_ok=True)

    csv_files = glob.glob(os.path.join(input_dir, "*.csv"))

    for src in csv_files:

        filename = os.path.basename(src)
        dst = os.path.join(archive_dir, filename)

        try:
            shutil.move(src, dst)
            logging.info(f"Archived {filename}")

        except Exception as error:
            logging.warning(f"Could not archive {filename}: {error}")
