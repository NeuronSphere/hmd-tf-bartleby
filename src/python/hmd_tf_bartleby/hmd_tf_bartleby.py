import shutil
import tempfile
import logging
import sys
import os
import json
from pathlib import Path
from subprocess import run
import urllib

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

    repo_name = os.environ.get("HMD_DOC_REPO_NAME")
    pip_user = os.environ.get("PIP_USERNAME")
    pip_pwd = os.environ.get("PIP_PASSWORD")

    def install_doc_repo(tmpdir):
        logger.info(f"Installing {repo_name} package to allow import..")
        path = Path(tmpdir) / "packages"
        if Path(pip_user).exists() and Path(pip_pwd).exists():
            with open(Path(pip_user), "r") as secret:
                pip_username = secret.readline()
            with open(Path(pip_pwd), "r") as secret:
                pip_password = secret.readline()
        else:
            pip_username = pip_user
            pip_password = pip_pwd
        if pip_username and pip_password:
            install = run(
                [
                    "pip",
                    "install",
                    "--extra-index-url",
                    f"https://{pip_username}:{urllib.parse.quote(pip_password)}@hmdlabs.jfrog.io/artifactory/api/pypi/hmd_pypi/simple",
                    "--target",
                    path,
                    repo_name,
                ]
            )
            logger.info(
                f"Install process completed with exit code: {install.returncode}"
            )
        else:
            raise Exception("Autodoc requires pip credentials as secrets.")

    def get_index(path: Path):

        with path.open("r") as index:
            text = index.readlines()
            i = [text.index(x) for x in text if x == "Indices and tables\n"][0]
            text.insert(
                i,
                f".. autosummary::\n   :toctree: _autosummary\n   :recursive:\n\n   {repo_name.replace('-', '_')}\n\n",
            )
        return text

    def add_package_to_index(path: Path):

        index = [
            file
            for file in os.scandir(path)
            if os.path.basename(Path(file)) == "index.rst"
        ]
        if Path(index[0]).exists():
            logger.info("Index found..")
            text = get_index(Path(index[0]))
            with Path(index[0]).open("w") as index:
                index.writelines(text)

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

            autodoc = os.environ.get("AUTODOC")
            if autodoc:
                install_doc_repo(tmpdir)
                logger.info("Adding package to index..")
                add_package_to_index(Path(os.path.join(tmpdir, "source")))

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

    # install_doc_repo()
    do_transform()
    logger.info("Transform complete.")
