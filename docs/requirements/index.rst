.. Bartleby transform requirements

Requirements
============

What the Bartleby transform image must do, written as `sphinx-needs
<https://sphinx-needs.readthedocs.io/>`_ items so that each one can be linked to
the tests that verify it. The generated :doc:`traceability` page carries the
matrix.

This is the standing baseline: it describes the transform as it is meant to
behave, not the history of how it got there. Proposals for *changes* remain
NERDs under :doc:`../proposals/index`, and a NERD links to the requirements it
adds or amends.

How this works
--------------

**Requirements** are ``.. req::`` items. Where the way a requirement is met is
itself worth pinning down, a ``.. spec::`` item links to it.

**IDs** are area-coded::

    HMD_TF_BARTLEBY_REQ_<AREA>_<NNN>

.. list-table::
   :header-rows: 1
   :widths: 20 80

   * - Area
     - Covers
   * - ``BUILD``
     - Running a builder over the mounted repository and producing its output.
   * - ``BRAND``
     - The confidentiality statement, logos, and the copyright notice.
   * - ``SEL``
     - Choosing the root document and the builder to run.
   * - ``CONV``
     - Converting the rendered documentation to Word and PowerPoint.

**Tests declare their own coverage**, in the test source rather than in a
separate list that would drift. This repository's tests are Robot suites, which
declare it in ``[Tags]``:

.. code-block:: robotframework

    Confidentiality Statement Exists In PDF
        [Tags]    REQ_BRAND_001

The short form is used in annotations; the tooling expands it to the full ID.
``reqtrace`` also reads Go tests' ``// Requirements:`` doc comments, which
matters only if this repository ever grows Go.

**Both directions are enforced.** ``make check`` runs ``reqtrace -check``, which
fails on:

- a requirement no test verifies,
- a test that declares no requirement,
- a reference to a requirement that does not exist,
- a duplicate requirement ID,
- a ``:links:`` target that does not exist,
- a stale :doc:`traceability` page.

``reqtrace`` needs neither Docker nor Sphinx, so that check holds on a laptop
and in CI. Running the *tests* does need Docker, since they render through the
container.

**Exemptions** exist for requirements no automated test can reasonably cover.
Such a requirement is tagged ``trace-exempt`` and has to say in its own text how
it *is* verified.

**Keywords.** The obligation in each requirement is written with ``shall``, in
the sense given by :rfc:`2119`: ``shall`` and ``must`` are absolute
requirements, ``should`` is a recommendation that needs a stated reason to
ignore, and ``may`` is optional. The baseline uses ``shall`` for anything a test
can fail on, and avoids ``should`` — a recommendation nothing can verify does
not belong in a requirements baseline.

.. toctree::
   :maxdepth: 2

   build
   brand
   selection
   conversion
   traceability
