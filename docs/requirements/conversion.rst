.. Conversion requirements

Word and PowerPoint
===================

Sphinx has no writer for either format, so these builders render the
documentation and then convert it with pandoc. See
:doc:`../proposals/NERD005_Word_And_Powerpoint_Output` for why pandoc rather
than a Sphinx docx extension.

.. req:: Produce a Word document
    :id: HMD_TF_BARTLEBY_REQ_CONV_001
    :status: implemented

    The ``docx`` builder shall write a Word document containing the
    documentation's headings, prose, and tables.

.. req:: Produce a slide deck, one slide per section
    :id: HMD_TF_BARTLEBY_REQ_CONV_002
    :status: implemented

    The ``pptx`` builder shall write a PowerPoint deck in which each section
    begins a new slide, rather than the whole document arriving on one.

.. req:: Name the outputs like the PDF
    :id: HMD_TF_BARTLEBY_REQ_CONV_003
    :status: implemented

    Both shall be named from ``DOCUMENT_TITLE``, or the document repository and
    its version, and shall be lifted to the top of the output directory — the
    same treatment the PDF gets, so a caller collecting artifacts does not need
    to know which builder produced which shape of tree.

.. req:: Leave the theme behind
    :id: HMD_TF_BARTLEBY_REQ_CONV_004
    :status: implemented

    The converted output shall contain the document and nothing else — no
    sidebar, no navigation, no search box, and no heading permalink glyphs.

    pandoc converts a whole HTML page, so handing it the themed output puts the
    furniture in the Word document, and in PowerPoint the sidebar's heading
    outranks the document's own title and takes the first slide.

.. spec:: The converted document is the body, not the page
    :id: HMD_TF_BARTLEBY_REQ_CONV_004_SPEC001
    :links: HMD_TF_BARTLEBY_REQ_CONV_004
    :status: implemented

    The builders shall convert an extracted document body rather than the
    rendered page, and that extraction shall be independent of the theme in use
    — a theme change shall not put furniture back into the output.

    Sphinx also wraps every section in ``<section>``, which pandoc reads as a
    Div; a heading inside a Div is not a top-level block and starts no slide, so
    the wrappers are removed as part of the same step.

.. spec:: Styles come from a reference document
    :id: HMD_TF_BARTLEBY_REQ_CONV_001_SPEC001
    :links: HMD_TF_BARTLEBY_REQ_CONV_001
    :status: implemented
    :tags: trace-exempt

    ``HMD_DOC_REFERENCE_DOCX`` and ``HMD_DOC_REFERENCE_PPTX`` shall name a
    document whose styles the output adopts — fonts, colours, heading styles, a
    title slide — so output can carry an organisation's template rather than
    pandoc's defaults.

    *Verification:* by manual run. Covering it needs a reference ``.docx``
    fixture in the test inputs, which is a binary file the suite does not
    currently carry; that fixture is the right follow-up.
