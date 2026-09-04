.. NERD004 Overridable Branding

NERD004 Overridable Branding
=============================

A repository documenting something other than NeuronSphere needs its own notice
and its own mark. Two things stood in the way: the copyright line was assembled
from a fixed format, and the transform set a logo through a mechanism a caller
could not see or turn off.

.. req:: The copyright line must be replaceable in full
    :id: HMD_TF_BARTLEBY_NERD004
    :status: implemented

    The footer notice shall be settable outright, not only through the company
    name inside a fixed ``<year>, <company>`` format. ``HMD_DOC_COPYRIGHT``
    replaces the line; ``HMD_DOC_AUTHOR`` replaces the author. Both fall back to
    the previous behaviour, so nothing changes for a caller that sets neither.

The line was::

    company_name_acronym = os.environ.get("HMD_DOC_COMPANY_NAME", "HMD Labs")
    copyright = "{}, {}".format(datetime.date.today().year, company_name_acronym)

which allows "2026, GitLab Inc." and nothing else — no notice without a year, no
"All rights reserved", no third-party attribution.

.. spec:: The manifest can set it too
    :id: HMD_TF_BARTLEBY_NERD004_SPEC001
    :links: HMD_TF_BARTLEBY_NERD004
    :status: implemented

    Because per-repo ``bartleby.roots.<root>.config`` is applied to Sphinx
    globals after this file runs, ``copyright`` and ``author`` set there already
    win. That is the better home for a permanent per-repository notice; the
    environment variables suit a pipeline that renders several repositories.

.. req:: The HTML and PDF logos are separate settings
    :id: HMD_TF_BARTLEBY_NERD004_REQ002
    :status: implemented

    ``HTML_DEFAULT_LOGO`` shall select the HTML logo and ``PDF_DEFAULT_LOGO`` the
    PDF cover image, independently.

They were the same variable, assigned twice::

    default_html_logo = os.environ.get("HTML_DEFAULT_LOGO", default_logo)
    default_html_logo = os.environ.get("PDF_DEFAULT_LOGO", default_logo)

The second assignment won, so ``HTML_DEFAULT_LOGO`` did nothing and the HTML
sidebar logo was whatever the PDF variable said.

.. req:: Exactly one logo renders
    :id: HMD_TF_BARTLEBY_NERD004_REQ003
    :status: implemented

    When a repository sets ``html_logo``, that shall be the only logo in the
    output. The theme's default shall step aside rather than render above or
    below it.

Sphinx and the theme have separate logo mechanisms and both were live. This
transform always set ``html_theme_options["logo"]``, which alabaster renders in
its sidebar; a repository setting ``html_logo`` additionally got Sphinx's own
sidebar logo block. Nothing turned the first off, so the output carried both —
the repository's mark stacked above the NeuronSphere swoosh.

.. spec:: Reconcile after the per-repo config is applied
    :id: HMD_TF_BARTLEBY_NERD004_REQ003_SPEC001
    :links: HMD_TF_BARTLEBY_NERD004_REQ003
    :status: implemented

    ``html_logo`` usually arrives from the manifest, which is applied to globals
    at the end of ``conf.py``. The reconciliation therefore runs after that, and
    logs which logo it kept, so the choice is visible in the build log rather
    than inferred from the page.
