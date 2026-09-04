.. NERD003 Diagnosable Build Failures

NERD003 Diagnosable Build Failures
===================================

.. req:: A failed document build must fail the transform
    :id: HMD_TF_BARTLEBY_NERD003
    :status: implemented

    When Sphinx exits non-zero, the transform shall exit non-zero. Every caller —
    the CLI, CI, the transform manager — decides success from the container's exit
    code, so a document that does not compile must not be reported as a
    successful build.

The transform captured the Sphinx exit code and wrote it to the log, then carried
on and exited 0::

    with open(log_file, "w") as log:
        sphinx = run(cmd_ar, text=True, cwd=tmpdir, stderr=STDOUT, stdout=log)
    ...
    logger.info(f"Process completed with exit code: {sphinx.returncode}")

A repository whose root document did not exist produced ``make html`` exit 2, a
container exit of 0, and a CLI that printed "Done". The failure was visible only
to someone who opened the log and read it.

.. spec:: Raise after the artifacts are copied out
    :id: HMD_TF_BARTLEBY_NERD003_SPEC001
    :links: HMD_TF_BARTLEBY_NERD003
    :status: implemented

    The failure shall be raised *after* the logs and any partial output have been
    copied to the output mount, and the message shall name the log files. Failing
    earlier would leave nothing on the host to diagnose the failure with, which is
    the situation the reporting is meant to fix.

.. req:: The reason a build failed must be readable without wading
    :id: HMD_TF_BARTLEBY_NERD003_REQ002
    :status: implemented

    The transform shall write the diagnostics a person needs to the output mount,
    separated by kind, so that a failure can be understood from the files on the
    host without re-running the build with different flags.

The combined ``logs/<builder>.log`` is complete but long — Sphinx progress and,
for PDF, thousands of lines of ``latexmk`` output. The two or three lines that
explain a broken document are in there somewhere. LaTeX's own log, which is the
only place a PDF-specific failure is explained, was written inside the ``latex/``
build tree next to megabytes of static assets.

.. spec:: Sphinx warnings and errors get their own file
    :id: HMD_TF_BARTLEBY_NERD003_SPEC002
    :links: HMD_TF_BARTLEBY_NERD003_REQ002
    :status: implemented

    The transform shall pass ``-w <output>/logs/<builder>-warnings.log`` to
    ``sphinx-build`` through ``SPHINXOPTS``, preserving any ``SPHINXOPTS`` the
    caller already set. Sphinx then writes every warning and error to that file as
    well as to the combined log.

.. spec:: The LaTeX log is copied next to the other logs
    :id: HMD_TF_BARTLEBY_NERD003_SPEC003
    :links: HMD_TF_BARTLEBY_NERD003_REQ002
    :status: implemented

    After a PDF build, each ``latex/*.log`` shall be copied to
    ``logs/<builder>-latex-<name>.log``.

.. req:: The image must be buildable and runnable from a working tree
    :id: HMD_TF_BARTLEBY_NERD003_REQ003
    :status: implemented

    A change to this repository shall be testable without publishing an image and
    without the private package index: ``make image-local`` builds
    ``hmd-tf-bartleby:local`` from the working tree, and the CLI runs it with
    ``bartleby --image hmd-tf-bartleby:local``.

Debugging the transform previously meant either a release or reproducing the HMD
build tooling's staged context by hand. Neither is a loop anyone iterates in.

.. spec:: A development Dockerfile with no network dependency
    :id: HMD_TF_BARTLEBY_NERD003_SPEC004
    :links: HMD_TF_BARTLEBY_NERD003_REQ003
    :status: implemented

    ``src/docker/Dockerfile.dev`` shall take ``plantuml.jar`` from the build
    context and install the transform package from source. The Makefile stages the
    jar from an image already on the machine, falling back to a local Homebrew copy
    and then to a download.

    ``Dockerfile.local`` is left as it is, because the HMD docker build stages its
    context and depends on that shape.

.. spec:: The published download must fail loudly
    :id: HMD_TF_BARTLEBY_NERD003_SPEC005
    :links: HMD_TF_BARTLEBY_NERD003_REQ003
    :status: implemented

    The ``plantuml.jar`` download in the published Dockerfiles shall use ``curl
    -f`` with retries and verify the archive. Without ``-f``, a SourceForge error
    page is written to ``plantuml.jar`` and the build succeeds with a jar that is
    HTML — a failure that surfaces much later as an unrelated PlantUML error.
