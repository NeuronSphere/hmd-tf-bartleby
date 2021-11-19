import shutil
import tempfile
import logging
import sys
import os
import json
from pathlib import Path
from subprocess import run

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
        os.environ.get("TRANSFORM_INSTANCE_CONTEXT")
    )
    transform_nid = os.environ.get("TRANSFORM_NID")

    def do_transform():

        with tempfile.TemporaryDirectory() as tmpdir:
            logger.info("Copying sphinx config files..")
            shutil.copytree(
                src=input_content_path.parent / "doctools",
                dst=tmpdir,
                dirs_exist_ok=True,
            )
            logger.info("Copying raw docs..")
            shutil.copytree(
                src=input_content_path,
                dst=os.path.join(tmpdir, "source"),
                dirs_exist_ok=True,
            )

            logger.info(f"Executing: make {transform_instance_context['shell']}")
            cmd_ar = ["make"]
            if transform_instance_context["shell"] != "default":
                cmd_ar.extend(transform_instance_context["shell"].split(" "))
            sphinx = run(cmd_ar, text=True, cwd=tmpdir)

            logger.info("Copying generated docs..")
            shutil.copytree(
                src=os.path.join(tmpdir, "build"),
                dst=output_content_path,
                dirs_exist_ok=True,
            )

            shutil.rmtree(tmpdir)

        logger.info(f"Process completed with exit code: {sphinx.returncode}")

        logger.info(f"Transform_nid: {transform_nid}")
        logger.info(f"Transform_instance_context: {transform_instance_context}")

    do_transform()
    logger.info("Transform complete.")
