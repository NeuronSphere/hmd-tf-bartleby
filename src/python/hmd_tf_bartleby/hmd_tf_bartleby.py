import shutil
import stat
import tempfile
import logging
import sys
import os
import json
from contextlib import contextmanager
from pathlib import Path
from subprocess import run, STDOUT
from typing import List


@contextmanager
def cd(newdir):
    prevdir = os.getcwd()
    os.chdir(os.path.expanduser(newdir))
    try:
        yield
    finally:
        os.chdir(prevdir)


logging.basicConfig(
    stream=sys.stdout,
    format="%(levelname)s %(asctime)s - %(message)s",
    level=logging.ERROR,
)

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


def render_puml(files: List[str]):
    """

    :param files:
    :return:
    """
    # TODO allow options for puml outputs
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
            # TODO do something useful with stderr and out
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
        docs_exists = os.path.exists(input_content_path / "docs")

        with tempfile.TemporaryDirectory() as tmpdir:
            logger.info("Copying sphinx config files..")
            shutil.copytree(
                src=input_content_path.parent / "doctools",
                dst=tmpdir,
                dirs_exist_ok=True,
                ignore_dangling_symlinks=True,
            )
            # Copy global styles (from $HMD_HOME/bartleby/styles/<shell>/)
            shell = transform_instance_context.get("shell", "")
            global_styles_path = Path("/hmd_transform/global_styles") / shell
            if global_styles_path.exists():
                for subdir in ["_static", "_templates"]:
                    src = global_styles_path / subdir
                    if src.exists():
                        shutil.copytree(
                            src=src,
                            dst=os.path.join(tmpdir, "source", subdir),
                            dirs_exist_ok=True,
                            ignore_dangling_symlinks=True,
                        )
                conf_overrides = global_styles_path / "conf_overrides.json"
                if conf_overrides.exists():
                    os.environ["BARTLEBY_GLOBAL_CONF_OVERRIDES"] = (
                        conf_overrides.read_text()
                    )

            logger.info("Copying raw docs..")
            shutil.copytree(
                src=(
                    input_content_path
                    if not docs_exists
                    else input_content_path / "docs"
                ),
                dst=os.path.join(tmpdir, "source"),
                dirs_exist_ok=True,
                ignore_dangling_symlinks=True,
            )

            if docs_exists:
                shutil.copytree(
                    src=input_content_path,
                    dst=tmpdir,
                    ignore_dangling_symlinks=True,
                    dirs_exist_ok=True,
                )

            if os.path.exists(os.path.join(tmpdir, "Makefile")):
                os.remove(os.path.join(tmpdir, "Makefile"))
            shutil.copyfile(
                os.path.join(tmpdir, "HMD_Bartleby_Makefile"),
                os.path.join(tmpdir, "Makefile"),
            )
            st = os.stat(os.path.join(tmpdir, "Makefile"))
            os.chmod(os.path.join(tmpdir, "Makefile"), 777)

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

            shell = transform_instance_context["shell"]

            log_path = output_content_path / "logs"
            os.makedirs(log_path, exist_ok=True)
            log_file = log_path / f"{shell}.log"
            warning_file = log_path / f"{shell}-warnings.log"

            logger.info(f"Executing: make {shell}")
            # TODO: add option to extend this?
            cmd_ar = ["make"]
            if shell != "default":
                cmd_ar.extend(shell.split(" "))

            # Sphinx writes its warnings and errors to a file of their own as
            # well as to the combined log. The combined log is mostly latexmk
            # and Sphinx progress output, so the handful of lines that explain a
            # broken document are easy to miss in it. SPHINXOPTS is honoured by
            # HMD_Bartleby_Makefile, and anything the caller already set there
            # is preserved.
            build_env = dict(os.environ)
            sphinx_opts = build_env.get("SPHINXOPTS", "").strip()
            build_env["SPHINXOPTS"] = f"{sphinx_opts} -w {warning_file}".strip()

            logger.info(f"Executing:  {cmd_ar}")
            with open(log_file, "w") as log:
                sphinx = run(
                    cmd_ar, text=True, cwd=tmpdir, stderr=STDOUT, stdout=log, env=build_env
                )

            if Path(os.path.join(tmpdir, "build")).exists():
                logger.info("Copying generated docs..")
                shutil.copytree(
                    src=os.path.join(tmpdir, "build"),
                    dst=output_content_path,
                    dirs_exist_ok=True,
                )
                # The document itself is what the caller wants; the rest of
                # the build tree is scaffolding. Lift it to the top of the
                # output so it does not have to be dug out of latex/ or docx/.
                for pattern in ("latex/*.pdf", "docx/*.docx", "pptx/*.pptx"):
                    for artifact in output_content_path.rglob(pattern):
                        shutil.copy2(artifact, output_content_path / artifact.name)

                # LaTeX explains PDF failures that Sphinx cannot: an undefined
                # control sequence, a missing font, a box it could not set. That
                # log is otherwise buried in the latex build tree next to
                # megabytes of static assets.
                for latex_log in output_content_path.rglob("latex/*.log"):
                    shutil.copy2(latex_log, log_path / f"{shell}-latex-{latex_log.name}")
            else:
                logger.info("No generated docs to copy..")

            shutil.rmtree(tmpdir)

        logger.info(
            f"Process completed with exit code: {sphinx.returncode}\n"
            f"Logs are available in the following location: "
            f"./target/bartleby/logs/"
        )

        logger.info(f"nid_context: {nid_context}")
        logger.info(f"Transform_instance_context: {transform_instance_context}")

        # A document that does not build is a failed transform. Until now the
        # exit code was only logged, so the container exited 0 and every caller —
        # the CLI, CI, the transform manager — reported a broken build as a
        # success. Raising here happens after the logs and any partial output
        # have been copied out, so the failure is diagnosable.
        if sphinx.returncode != 0:
            hint = f"See ./target/bartleby/logs/{shell}.log"
            if warning_file.exists() and warning_file.stat().st_size > 0:
                hint += f" and ./target/bartleby/logs/{warning_file.name}"
            raise RuntimeError(
                f"Document build failed: `{' '.join(cmd_ar)}` exited "
                f"{sphinx.returncode}. {hint}"
            )

    # install_doc_repo()
    do_transform()
    logger.info("Transform complete.")
