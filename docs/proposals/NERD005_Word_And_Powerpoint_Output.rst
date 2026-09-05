.. NERD005 Word and PowerPoint Output

NERD005 Word and PowerPoint Output
==================================

.. req:: Render documentation to Word and PowerPoint
    :id: HMD_TF_BARTLEBY_NERD005
    :status: completed

    The transform shall offer ``docx`` and ``pptx`` builders, so that
    documentation maintained as reStructuredText can be handed to people who
    work in Word and PowerPoint without being rewritten there.

Documentation that only exists as a web page or a PDF gets copied into a Word
document by hand the first time somebody needs to comment on it, and from then
on the copy is the version people edit. The same is true of slides: a design
review wants a deck, and the deck is usually assembled by pasting from the docs
and immediately going stale.

Both are conversions of a document that already exists, so the transform should
do them.

Why not a Sphinx extension
--------------------------

Sphinx has no docx writer of its own, and the community extensions are
abandoned: ``docxbuilder`` was last released in 2020, ``sphinx-docxbuilder`` in
2019, and ``sphinxcontrib-docxbuilder`` never left ``0.0.1alpha``.
``docxbuilder`` declares ``Sphinx>=1.7.6`` with no upper bound, so it installs
against Sphinx 9 and nobody has checked what it does there. There is no pptx
extension at all.

Pandoc is maintained, converts to both formats, and takes a reference document
for styling — which is the requirement behind most requests for Word output,
since what people actually want is their own template. It costs one system
package in the image and no Python dependency.

.. spec:: Convert from rendered HTML
    :id: HMD_TF_BARTLEBY_NERD005_SPEC001
    :links: HMD_TF_BARTLEBY_NERD005
    :status: completed

    The builders shall convert Sphinx's ``singlehtml`` output rather than its
    LaTeX. HTML holds the whole document in one file with headings, tables and
    images intact, and pandoc's HTML reader is markedly more reliable than its
    LaTeX reader on the macros Sphinx emits.

.. spec:: Convert the body, not the page
    :id: HMD_TF_BARTLEBY_NERD005_SPEC002
    :links: HMD_TF_BARTLEBY_NERD005
    :status: completed

    pandoc converts an entire page. Handing it the themed output puts the
    sidebar, the navigation, the search box and the heading permalink glyphs
    into the Word document; in PowerPoint the theme's own ``<h1>`` outranks the
    document title and takes the first slide. The builders shall therefore
    convert an extracted document body.

    Sphinx wraps each section in ``<section>``, which pandoc reads as a Div.
    A heading inside a Div is not a top-level block, so pandoc's pptx writer
    starts no slide at it and the entire document lands on a single slide
    whatever ``--slide-level`` is set to. The extraction removes those wrappers.

    Both defects were found by inspecting the produced files rather than by the
    builders failing: each one exited zero and wrote a plausible document.

.. spec:: Adopt the caller's styles
    :id: HMD_TF_BARTLEBY_NERD005_SPEC003
    :links: HMD_TF_BARTLEBY_NERD005
    :status: completed

    ``HMD_DOC_REFERENCE_DOCX`` and ``HMD_DOC_REFERENCE_PPTX`` shall name a
    reference document whose styles the output adopts. Without one, pandoc's
    defaults apply.

Requirements added
------------------

The standing requirements are in :doc:`../requirements/conversion` —
``REQ_CONV_001`` to ``REQ_CONV_004``. The proposal is recorded here; the
obligations live there, where the traceability check can enforce them.
