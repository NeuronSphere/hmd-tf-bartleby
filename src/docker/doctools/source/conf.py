# Configuration file for the Sphinx documentation builder.
#
# This file only contains a selection of the most common options. For a full
# list see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Path setup --------------------------------------------------------------

# If extensions (or modules to document with autodoc) are in another directory,
# add these directories to sys.path here. If the directory is relative to the
# documentation root, use os.path.abspath to make it absolute, like shown here.
#
import os
import sys

sys.path.insert(0, os.path.abspath('../packages'))
# sys.path.insert(0, '/code/src/python')
# sys.path.insert(0, '/code/packages')
print(sys.path)

# -- Project information -----------------------------------------------------
company_name_acronym = 'HMD'
repo_name = os.environ.get("HMD_DOC_REPO_NAME")
repo_version = os.environ.get("HMD_DOC_REPO_VERSION")
project = '{} Labs project: {}'.format(company_name_acronym, repo_name)
copyright = '2021, {} Labs'.format(company_name_acronym)
author = '{} Labs'.format(company_name_acronym)

# The full version, including alpha/beta/rc tags
release = repo_version


# -- General configuration ---------------------------------------------------

# Add any Sphinx extension module names here, as strings. They can be
# extensions coming with Sphinx (named 'sphinx.ext.*') or your custom
# ones.
extensions = [
    'sphinx_copybutton',
    'sphinxcontrib.plantuml',
    'sphinx.ext.autodoc',
    'sphinx.ext.autosummary'
]

# autodoc default options
autodoc_default_options = {
    'members': True,
    'undoc-members': True,
    'private_members': True,
    'imported_members': False
}

# autosummary_mock_imports = [
#     "hmd_lang_librarian",
#     "hmd_graphql_client",
#     "hmd_schema_loader",
#     "hmd_meta_types",
#     "hmd_lang_device",
#     "hmd_lang_device_librarian",
#     "hmd_lang_case",
#     "boto3",
#     "hmd_lib_librarian_client",
#     "hmd_entity_storage",
#     "hmd_lib_naming",
#     "hmd_cli_tools",
#     "hmd_graphql",
#     "hmd_lang_naming"
# ]

# autodoc check for signatures within source code
autodoc_docstring_signature = True

autosummary_generate = True

# Add any paths that contain templates here, relative to this directory.
templates_path = ['_templates']

# List of patterns, relative to source directory, that match files and
# directories to ignore when looking for source files.
# This pattern also affects html_static_path and html_extra_path.
exclude_patterns = []

# path to jar file used for generating puml diagrams
plantuml = 'java -jar /usr/local/bin/plantuml.jar'


# -- Options for HTML output -------------------------------------------------

# The theme to use for HTML and HTML Help pages.  See the documentation for
# a list of builtin themes.
#
html_theme = 'alabaster'

# Add any paths that contain custom static files (such as style sheets) here,
# relative to this directory. They are copied after the builtin static files,
# so a file named "default.css" will overwrite the builtin "default.css".
html_static_path = ['_static']

# -- Options for LaTeX output -------------------------------------------------

# The theme to use for LaTeX pages.  See the documentation for
# a list of builtin themes.
#
latex_theme = 'howto'

# other elements used in latex pdf generation
latex_elements = {
    'atendofbody': 'HMD Labs Confidential – This document contains information that is confidential and proprietary. Neither this document nor the information herein may be reproduced, used, or disclosed to or for the benefit of any third party without the prior written consent of HMD Labs.'
}