import shutil
import tempfile
import logging
import sys
import os
import json
from pathlib import Path
from subprocess import run, STDOUT
from typing import List
from hmd_cli_tools.hmd_cli_tools import cd


logging.basicConfig(
    stream=sys.stdout,
    format="%(levelname)s %(asctime)s - %(message)s",
    level=logging.ERROR,
)

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


def render_puml(files: List[str]):
    input_content_path = Path("/hmd_transform/input")
    output_content_path = Path("/hmd_transform/output")
    with cd(input_content_path):
        for file in files:
            command = [
                "java",
                "-jar",
                "/usr/local/bin/plantuml.jar",
                "-o",
                output_content_path,
                file,
            ]
            process = run(command)
            if process.returncode != 0:
                raise Exception(f"Puml generation failed for {file}")
    logger.info("Puml generation completed.")


def entry_point():

    # initialize variables for transform I/O
    input_content_path = Path("/hmd_transform/input")
    output_content_path = Path("/hmd_transform/output")

    transform_instance_context = json.loads(
        os.environ.get("TRANSFORM_INSTANCE_CONTEXT")
    )
    nid_context = os.environ.get("NID_CONTEXT")

    repo_name = os.environ.get("HMD_DOC_REPO_NAME")
    pip_conf = os.environ.get("PIP_CONF")

    def install_doc_repo(tmpdir, name):
        logger.info(f"Installing {name} package to allow import..")
        path = Path(tmpdir) / "packages"
        if pip_conf:
            if Path(pip_conf).exists():
                pip_path = os.path.join(Path.home(), ".pip")
                if not Path(pip_path).exists():
                    os.makedirs(pip_path)
                    shutil.copyfile(pip_conf, Path.home() / ".pip" / "pip.conf")
                install = run(["pip", "install", "--target", path, name])
                logger.info(
                    f"Install process completed with exit code: {install.returncode}"
                )
            else:
                raise Exception("Autodoc requires pip credentials as secrets.")

    def get_index(path: Path, name, trunc=False):

        with path.open("r") as index:
            text = index.readlines()
            name = name.replace("-", "_")
            i = [text.index(x) for x in text if name in x]
            if len(i) > 0:
                i = i[0]
                text.insert(i, f".. autosummary::\n   :toctree: _autosummary\n\n")
                i = [text.index(x) for x in text if x == "Indexes and tables\n"][0]
            else:
                i = [text.index(x) for x in text if x == "Indexes and tables\n"][0]
                text.insert(
                    i,
                    f".. autosummary::\n   :toctree: _autosummary\n   :recursive:\n\n   {name}\n\n",
                )
            if trunc:
                del text[i:]
        return text

    def add_package_to_index(path: Path, name, trunc=False):

        index = [
            file
            for file in os.scandir(path)
            if os.path.basename(Path(file)) == "index.rst"
        ]
        if Path(index[0]).exists():
            logger.info("Index found..")
            text = get_index(Path(index[0]), name, trunc)
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
            if autodoc == "True":
                names = repo_name.split(",")
                if len(names) > 1:
                    for name in names:
                        install_doc_repo(tmpdir, name)
                        logger.info("Adding package to index..")
                        add_package_to_index(
                            Path(os.path.join(tmpdir, "source", name)), name, True
                        )
                else:
                    install_doc_repo(tmpdir, repo_name)
                    logger.info("Adding package to index..")
                    add_package_to_index(
                        Path(os.path.join(tmpdir, "source")), repo_name
                    )

            log_path = output_content_path / "logs"
            os.makedirs(log_path, exist_ok=True)
            log_file = log_path / f"{transform_instance_context['shell']}.log"

            logger.info(f"Executing: make {transform_instance_context['shell']}")
            # TODO: add option to extend this?
            cmd_ar = ["make"]
            if transform_instance_context["shell"] != "default":
                cmd_ar.extend(transform_instance_context["shell"].split(" "))
            with open(log_file, "w") as log:
                sphinx = run(cmd_ar, text=True, cwd=tmpdir, stderr=STDOUT, stdout=log)

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

        logger.info(
            f"Process completed with exit code: {sphinx.returncode}\n"
            f"Log file is available in the following location: "
            f"./target/bartleby/{transform_instance_context['shell']}.log"
        )

        logger.info(f"nid_context: {nid_context}")
        logger.info(f"Transform_instance_context: {transform_instance_context}")

    # install_doc_repo()
    do_transform()
    logger.info("Transform complete.")
