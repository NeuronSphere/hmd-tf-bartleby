.. NERD006 RevealJS PDF Export

NERD006 RevealJS PDF Export
============================

.. req:: Export a RevealJS deck as a slide-accurate PDF
    :id: HMD_TF_BARTLEBY_NERD006
    :status: proposed

    A ``revealjs`` root shall be able to produce a PDF of the deck — one page
    per slide, styled the same as the HTML — as a first-class bartleby output,
    without a manual step outside the transform.

The ``pdf`` builder already exists, but it renders Sphinx's LaTeX "manual"
output: chapters, a table of contents, and running headers meant for prose
documentation. It has no relationship to a ``revealjs`` root and cannot
produce a deck — running it against a presentation's root document yields a
paginated report, not slides. Today, getting a PDF of a reveal.js deck means
building the HTML and then converting it by hand outside bartleby entirely,
which is exactly what this proposal removes.

Why a browser, not a second LaTeX path
---------------------------------------

reveal.js ships its own print stylesheet, activated by a ``?print-pdf`` query
parameter: it linearizes the deck into one full-page block per slide, sized to
the deck's own ``width``/``height`` config via an ``@page`` rule. A headless
Chromium visiting the built HTML with that query parameter and printing to PDF
reproduces the deck exactly as authored — same theme, same fonts, same
tables — because it *is* the deck, not a re-render of the source through a
different toolchain. LaTeX has no reveal.js reader and would require
rebuilding the deck's layout logic from scratch.

The image already carries a headless-browser dependency shape via its other
conversions (pandoc for the ``docx``/``pptx`` builders, see
:doc:`NERD005_Word_And_Powerpoint_Output`), so adding one more converter that
runs entirely inside the existing Docker build is consistent with how those
were justified.

.. spec:: Trigger PDF export from the revealjs root's config
    :id: HMD_TF_BARTLEBY_NERD006_SPEC001
    :links: HMD_TF_BARTLEBY_NERD006
    :status: proposed

    A ``revealjs`` root's ``config`` shall accept a ``revealjs_export_pdf``
    boolean. When true, the transform shall produce the PDF alongside the
    HTML in the same build invocation, using the root's existing
    ``revealjs_script_conf`` width/height so the two outputs stay in sync
    without a second place to configure slide dimensions.

.. spec:: Render inside the transform's own container
    :id: HMD_TF_BARTLEBY_NERD006_SPEC002
    :links: HMD_TF_BARTLEBY_NERD006
    :status: proposed

    The conversion shall run inside the existing Docker build — a headless
    Chromium (or an equivalent reveal.js-to-PDF tool such as decktape,
    installed via the container's own network access rather than the
    caller's machine) added to the image — so callers gain PDF export without
    installing anything locally. This was the gap hit building a deck by hand
    outside bartleby: no local browser automation is guaranteed to exist on
    the machine invoking ``bartleby slides``, and any host-side tool choice
    (decktape via npm, headless Chrome print-to-pdf) is a workaround for the
    same reason the ``docx``/``pptx`` builders exist — the conversion belongs
    where the build already happens.

.. spec:: Name and place the output like the other builders
    :id: HMD_TF_BARTLEBY_NERD006_SPEC003
    :links: HMD_TF_BARTLEBY_NERD006
    :status: proposed

    The PDF shall be written as ``<root_doc>.pdf`` alongside
    ``<root_doc>.html`` in the ``revealjs`` output directory, mirroring the
    existing HTML output convention rather than introducing a new output
    layout or a separate builder name to select.
