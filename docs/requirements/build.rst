.. Build requirements

Running a Build
===============

The transform is handed a repository on ``/hmd_transform/input`` and a place to
put the results on ``/hmd_transform/output``, and told which builder to run. What
follows is what it owes the caller in return.

.. req:: Render the mounted repository with the requested builder
    :id: HMD_TF_BARTLEBY_REQ_BUILD_001
    :status: implemented

    Given a repository on the input mount and a builder named in
    ``TRANSFORM_INSTANCE_CONTEXT``, the transform shall render that
    repository's ``docs/`` with that builder and write the result to the output
    mount.

.. req:: Produce HTML the caller can serve
    :id: HMD_TF_BARTLEBY_REQ_BUILD_002
    :status: implemented

    The ``html`` builder shall write one HTML file per source document under
    ``html/``, named after the source document.

.. req:: Produce a single PDF
    :id: HMD_TF_BARTLEBY_REQ_BUILD_003
    :status: implemented

    The ``pdf`` builder shall write one PDF named after the document repository
    and its version, and shall leave the LaTeX it was built from beside it so a
    failure can be inspected.

.. req:: Fail when the document build fails
    :id: HMD_TF_BARTLEBY_REQ_BUILD_004
    :status: implemented
    :tags: trace-exempt

    A failed document build shall exit non-zero and name the log files that
    explain it. Exiting zero on a failed build is worse than failing, because
    the caller ships a broken or partial document believing it succeeded.

    *Verification:* by inspection and manual run — see NERD003, which records
    the defect this replaced. Exercising it needs a repository with a
    deliberately broken document, which the Robot suite does not yet carry; the
    gap is real and this exemption is a placeholder for a test, not a
    substitute for one.

.. req:: Leave the logs where the caller can read them
    :id: HMD_TF_BARTLEBY_REQ_BUILD_005
    :status: implemented
    :tags: trace-exempt

    The transform shall write Sphinx's output, its warnings, and LaTeX's log for
    a PDF build to ``logs/`` on the output mount, so that a diagnosis needs
    neither a rerun nor a shell in the container.

    *Verification:* by inspection and manual run; the same missing failing-build
    fixture as ``REQ_BUILD_004``.
