import shutil
import tempfile
import logging
import sys
import os
import json
from pathlib import Path
from subprocess import run
import urllib.parse
from pip._vendor import pkg_resources

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
    nid_context = os.environ.get("NID_CONTEXT")

    def get_index(path: Path, tmpdir):

        text = []
        with path.open("r") as index:
            text = index.readlines()
            i = [text.index(x) for x in text if x == "Indices and tables\n"][0]
            text.insert(i, ".. autosummary::\n   :toctree: modules\n\n")
            mods = get_modules(tmpdir)
            mod_string = "".join(mods)
            text.insert(i + 1, f"{mod_string}\n")
            logger.info(f"new text: {text}")
        return text

    def get_modules(tmpdir):
        logger.info("Getting modules..")
        mods = []
        for root, dirs, files in os.walk("/code/src/python"):
            if "__init__.py" in files:
                files.remove("__init__.py")
                for file in files:
                    mods.append(
                        f"   {os.path.join(root, file).replace('/code/src/python/', '').replace('/', '.').replace('.py', '')}\n"
                    )
        return mods

    def add_modules_to_index(path: Path):

        index = [
            file
            for file in os.scandir(path)
            if os.path.basename(Path(file)) == "index.rst"
        ]
        logger.info("Index found..")
        if Path(index[0]).exists():
            text = get_index(Path(index[0]), path)
            with Path(index[0]).open("w") as index:
                index.writelines(text)

    def do_transform(repo_docs: Path):

        with tempfile.TemporaryDirectory() as tmpdir:
            logger.info("Copying sphinx config files..")
            shutil.copytree(
                src=input_content_path.parent / "doctools",
                dst=tmpdir,
                dirs_exist_ok=True,
            )
            logger.info("Copying raw docs..")
            shutil.copytree(
                src=repo_docs, dst=os.path.join(tmpdir, "source"), dirs_exist_ok=True
            )

            autodoc = os.environ.get("AUTODOC")
            if autodoc:
                logger.info("Adding modules to index..")
                add_modules_to_index(Path(os.path.join(tmpdir, "source")))

            logger.info(f"Executing: make {transform_instance_context['shell']}")
            cmd_ar = ["make"]
            if transform_instance_context["shell"] != "default":
                cmd_ar.extend(transform_instance_context["shell"].split(" "))
            sphinx = run(cmd_ar, text=True, cwd=tmpdir)

            if Path(os.path.join(tmpdir, "build")).exists():
                logger.info("Copying generated docs..")
                shutil.copytree(
                    src=os.path.join(tmpdir, "build"),
                    dst=output_content_path,
                    dirs_exist_ok=True,
                )
            else:
                logger.info("No generated docs to copy..")

            shutil.rmtree(tmpdir)

        logger.info(f"Process completed with exit code: {sphinx.returncode}")

        logger.info(f"nid_context: {nid_context}")
        logger.info(f"Transform_instance_context: {transform_instance_context}")

    input_contents = [x for x in os.listdir(input_content_path)]
    do_transform()
    logger.info("Transform complete.")
