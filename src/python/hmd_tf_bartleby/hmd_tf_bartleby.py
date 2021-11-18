import logging
import sys
import os
import json
from pathlib import Path
import shutil

logging.basicConfig(
    stream=sys.stdout,
    format="%(levelname)s %(asctime)s - %(message)s",
    level=logging.ERROR,
)

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)


def entry_point():

    # initialize variables for transform I/O
    input_content_path = Path("/hmd_transform/input")
    output_content_path = Path("/hmd_transform/output")

    transform_instance_context = json.loads(
        os.environ.get("TRANSFORM_INSTANCE_CONTEXT").replace("'", '"')
    )
    transform_nid = os.environ.get("TRANSFORM_NID")

    def do_transform():

        for x in os.listdir(input_content_path):
            logger.info(f"Processing input file {x}...")
            shutil.copy(
                input_content_path / x, output_content_path / "sample_output.txt"
            )

        secret_path = Path("/run/secrets")

        for x in os.listdir(secret_path):
            logger.info(f"This is how to locate a secret: {x} in {secret_path}")

        logger.info(f"Transform_nid: {transform_nid}")
        logger.info(f"Transform_instance_context: {transform_instance_context}")

    do_transform()
    logger.info("Transform complete.")
