.. Branding requirements

Branding
========

Documents carry the marks of whoever they belong to. Every one of these is the
caller's to set, and the defaults exist so that a repository which sets nothing
still produces something coherent — not so that the transform's own branding
appears on other people's documents.

.. req:: Stamp the confidentiality statement onto a PDF
    :id: HMD_TF_BARTLEBY_REQ_BRAND_001
    :status: implemented

    Where ``CONFIDENTIALITY_STATEMENT`` is set, its text shall appear in the
    rendered PDF.

.. req:: Take the confidentiality statement from the caller
    :id: HMD_TF_BARTLEBY_REQ_BRAND_002
    :status: implemented

    The statement shall be whatever the caller set, not a fixed string — two
    builds with different statements shall produce two differently stamped
    documents.

.. req:: Put a cover image on a PDF
    :id: HMD_TF_BARTLEBY_REQ_BRAND_003
    :status: implemented

    Where a logo is configured, it shall appear as the PDF's cover image, and
    the image the caller named shall be the one used.

.. req:: Put a logo in the HTML sidebar
    :id: HMD_TF_BARTLEBY_REQ_BRAND_004
    :status: implemented

    Where a logo is configured, it shall appear in the rendered HTML, and the
    image the caller named shall be the one used.

.. req:: Render one logo, not two
    :id: HMD_TF_BARTLEBY_REQ_BRAND_005
    :status: implemented
    :tags: trace-exempt

    Where a repository sets ``html_logo`` in its own configuration, that logo
    shall replace the theme's default rather than appearing alongside it, and
    the build log shall record which logo was kept.

    Sphinx and the theme have independent logo mechanisms. With both live, the
    output stacked the repository's mark above the transform's own — see NERD004.

    *Verification:* by manual run against ``glintf-design``, which sets
    ``html_logo`` in its manifest — the rendered page carried exactly one
    ``<img>`` and no reference to the theme's default. The Robot suite drives the
    transform through environment variables only, so covering this needs an
    input fixture with its own manifest config, which is the right follow-up.

.. req:: Let the caller set the copyright notice
    :id: HMD_TF_BARTLEBY_REQ_BRAND_006
    :status: implemented

    ``HMD_DOC_COPYRIGHT`` shall replace the footer notice outright, and
    ``HMD_DOC_AUTHOR`` the author. Assembling the notice as
    ``<year>, <company>`` allows one shape and no other — no notice without a
    year, no "All rights reserved", no third-party attribution.

.. spec:: A repository's own config wins
    :id: HMD_TF_BARTLEBY_REQ_BRAND_006_SPEC001
    :links: HMD_TF_BARTLEBY_REQ_BRAND_006
    :status: implemented
    :tags: trace-exempt

    ``copyright`` and ``author`` set in a repository's manifest config shall take
    precedence over the environment, since per-repository config is applied to
    Sphinx settings after ``conf.py`` runs. That is the better home for a
    permanent notice.

    *Verification:* by manual run against a repository that sets them —
    performed against ``glintf-design``. The Robot suite drives the transform
    through environment variables only, so it cannot reach this path.
