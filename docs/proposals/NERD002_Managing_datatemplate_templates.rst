.. NERD002 Managing Datatemplate Templates

NERD002 Managing Datatemplate Templates
========================================

.. req:: Specify Additional Templates Directories
    :id: HMD_TF_BARTLEBY_NERD002

    The default configuration for sphinx-doc contains a variable *template_directory* in the default conf.py, with
    the default value being a single entry '_templates'.

    The current Bartleby transform implementation (this project) includes a _templates directory in src/docker/doctools/source
    that is used by other plugins and is not designed for end-user extension.

    Bartleby should provide a mechanism for the user to have templates (.tmpl) files in any docs repository without modification
    to the core Bartleby installation or image.


.. spec:: Default extra template directory in projects
    :id: HMD_TF_BARTLEBY_NERD002_SPEC001
    :links: HMD_TF_BARTLEBY_NERD002
    :status: proposed

    In order to enable the use of re-usable/distinct datatemplate templates, the datatemplate plugin attempts to load
    templates from the *template_directory* variable.  We will update the default Bartleby conf.py to optionally update
    that value as follows.

    In the /docs directory of the project, if the user has created a directory called '_datatemplates',
    that directory should be added to the *template_directory* list, such that the datatemplates plugin
    will be able to load the templates.

.. spec:: Datatemplates templates directory specified in manifest
    :id: HMD_TF_BARTLEBY_NERD002_SPEC002
    :links: HMD_TF_BARTLEBY_NERD002; HMD_TF_BARTLEBY_NERD002_SPEC001
    :status: proposed

    In the Bartleby section of the standard neuronsphere project manifest, include an optional configuration section to
    add one or more additional template directories.  These directories should be additive to the available /docs/_templates directory
    behavior specified in HMD_TF_BARTLEBY_NERD002_SPEC001.


.. spec:: Datatemplates templates directory specified in envvars
    :id: HMD_TF_BARTLEBY_NERD002_SPEC003
    :links: HMD_TF_BARTLEBY_NERD002; HMD_TF_BARTLEBY_NERD002_SPEC002
    :status: proposed

    Specify an optional environment variable following the standard Bartleby configuration pattern:
    HMD_BARTLEBY__DATATEMPLATE_DATATEMPLATE_TEMPLATE_DIRECTORIES=comma separate list

    Note this implementation is not as simple as passing the environment variable *through* to the plugin,
    rather using a standard environment variable for this presents a more universal UX while hiding the details of
    conf.py variable manipulation.

    Also note that this behaviour is additive to HMD_TF_BARTLEBY_NERD002_SPEC002.


.. req:: Data Templates as external dependencies
    :id: HMD_TF_BARTLEBY_NERD003
    :links: HMD_TF_BARTLEBY_NERD002
    :status: draft

    Ideally, Bartleby could use libraries and capabilities from *hmd-mickey\** to package and share template libraries
    in the same way that *mickey* allows sharing template bundles.

    Template dependencies should be declared in the project manifest, and loaded/managed similar to how mickey
    manages external templates.  Perhaps this is a .bart_templates_cache?

