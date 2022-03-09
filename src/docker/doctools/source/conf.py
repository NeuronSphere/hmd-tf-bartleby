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
import datetime

sys.path.insert(0, os.path.abspath('../packages'))

# -- Project information -----------------------------------------------------
company_name_acronym = 'HMD'
repo_name = os.environ.get("HMD_DOC_REPO_NAME")
repo_version = os.environ.get("HMD_DOC_REPO_VERSION")
if len(repo_name.split(",")) == 1:
    project = 'NeuronSphere project: {}'.format(repo_name)
    release = repo_version
else:
    project = 'NeuronSphere projects'
    release = f"{os.environ.get('HMD_CUSTOMER_CODE', 'HMD')}-{os.environ.get('HMD_DID', 'aaa')}"
copyright = '{}, {} Labs'.format(datetime.date.today().year, company_name_acronym)
author = '{} Labs'.format(company_name_acronym)

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


autodoc_default_options = {
    'members': True,
    'undoc-members': True,
    'private_members': True,
    'imported_members': False,
    'member-order': 'bysource'
}

# autodoc check for signatures within source code
autodoc_docstring_signature = True

autosummary_generate = True


# docstring processing
def extra_processing(app, what, name, obj, options, lines):
    pass


def signature_processing(app, what, name, obj, options, signature, return_annotation):
    pass


def setup(app):
    app.connect("autodoc-process-docstring", extra_processing)
    app.connect("autodoc-process-signature", signature_processing)


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
# html_logo = f"./{html_static_path[0]}/Neuron_Sphere_Symbol_Color2.png"
html_theme_options = {
    'logo': 'Neuron_Sphere_Logo_RGB_Color.png',
    'logo_name': True,
    'page_width': '1100px',
    'sidebar_width': '270px',
    'sidebar_header': '#191970',
    'sidebar_link': '#191970',
    'narrow_sidebar_bg': '#191970',
    'narrow_sidebar_link': '#ADD8E6',
    'link': '#191970',
    'link_hover': '#8B0000',
    'show_powered_by': False,
    'head_font_family': "'Gill Sans Light',sans-serif",
    'font_family': "'Gill Sans Light',sans-serif",
    'caption_font_family': "'Gill Sans Light',sans-serif",
    'pre_bg': '#F0F8FF',
    'note_bg': '#FFE4E1',
    'note_border': '#8B0000',
}

# -- Options for LaTeX output -------------------------------------------------

# The theme to use for LaTeX pages.  See the documentation for
# a list of builtin themes.
#
latex_theme = 'howto'

# other elements used in latex pdf generation
latex_elements = {
    'preamble': r'\usepackage{enumitem}\setlistdepth{99}\usepackage{charter}\usepackage[defaultsans]{lato}\usepackage{inconsolata}\setlength{\fboxsep}{6pt}',
    'makeindex': r'\usepackage[columns=1]{idxlayout}\makeindex',
    'atendofbody': r'\vspace*{\fill}\textit{HMD Labs Confidential – This document contains information that is confidential and proprietary. Neither this document nor the information herein may be reproduced, used, or disclosed to or for the benefit of any third party without the prior written consent of HMD Labs.}\pagebreak',
    'sphinxsetup': r'VerbatimColor={RGB}{240,248,255}, verbatimwithframe=false, noteBorderColor={RGB}{139,0,0}, InnerLinkColor={RGB}{25,25,112}, TitleColor={RGB}{25,25,112}, HeaderFamily='
}

latex_logo = f"./{html_static_path[0]}/NeuronSphereSwoosh_Short.jpg"
