.. Selection requirements

Choosing What to Build
======================

.. req:: Build the root document the caller asked for
    :id: HMD_TF_BARTLEBY_REQ_SEL_001
    :status: implemented

    Where ``TRANSFORM_INSTANCE_CONTEXT`` names a ``root_doc``, the transform
    shall build from that document rather than from ``index``, and the rendered
    document's title shall be that document's title.
