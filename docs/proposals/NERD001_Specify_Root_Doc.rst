.. NERD001 Specify Root Document

NERD001 Specify Root Document
==============================

.. req:: Specify Root Document
    :id: HMD_TF_BARTLEBY_NERD001

    Bartleby should accept a configuration option that specifies the ``root_doc`` configuration option passed to Sphinx.

.. spec:: Root document defined in Transform Context
    :id: HMD_TF_BARTLEBY_NERD001_SPEC001
    :links: HMD_TF_BARTLEBY_NERD001
    :status: proposed

    The root document name should be passed into the Bartleby transform via the Transform Context, like the ``shell`` option to choose a builder.
    It should default to ``'index'``.

Occasionally, you need to build multiple different output documents from the same NeuronSphere Project.
Bartleby only support building documents with the root document being ``docs/index.rst``.
This proposal is to allow the user to specify which document to use as the Sphinx ``root_doc`` configuration parameter via the Transform Context object.
We already pass in ``shell``, which equates to the builder to use. This will just be an optional additional key in that object of ``root`` and be the name of a document in the ``docs`` folder of the project.