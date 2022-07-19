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
from importlib import import_module
import inspect
import ast

sys.path.insert(0, os.path.abspath('../packages'))

# -- Project information -----------------------------------------------------
company_name_acronym = 'HMD'
repo_name = os.environ.get("HMD_DOC_REPO_NAME")
repo_version = os.environ.get("HMD_DOC_REPO_VERSION")
if len(repo_name.split(",")) == 1:
    project = 'NeuronSphere component: \n{}'.format(repo_name)
    release = repo_version
else:
    project = 'NeuronSphere components'
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
    'private-members': False,
    'imported-members': False,
    'exclude-members': '__init__',
    'member-order': 'bysource'
}

# autodoc check for signatures within source code
autodoc_docstring_signature = True

autosummary_generate = True


# docstring processing
def extra_processing(app, what, name, obj, options, lines):
    repo = name.split('.')[0]
    mod_name = repo.replace('-', '_')
    module = import_module(f"{mod_name}.{mod_name}")
    if hasattr(module, "setup"):
        setup = getattr(module, "setup")
    else:
        return lines
    custom_ops = dict(
        [[x.name, x] for x in ast.walk(ast.parse(inspect.getsource(setup))) if type(x).__name__ == 'FunctionDef']
    )
    for op in custom_ops:
        decs = custom_ops[op].decorator_list
        decs_dict = {}
        for dec in decs:
            kws = dec.keywords
            kw_dict = {}
            for kw in kws:
                if kw.arg == 'rest_path':
                    kw_dict.update({f"**{kw.arg}**": ast.parse(kw.value).value})
                elif kw.arg == 'rest_methods':
                    try:
                        kw_dict.update({f"**{kw.arg}**": ast.parse(kw.value).elts[0].value})
                    except Exception as e:
                        pass
                elif kw.arg == 'args':
                    try:
                        kw_dict.update(
                            {f"**{kw.arg}**": {ast.parse(kw.value).keys[0].value: ast.parse(kw.value).values[0].value}}
                        )
                    except Exception as e:
                        pass
            decs_dict.update({op: kw_dict})
        if op == method_name and len(decs_dict.get(op)) > 0:
            decorator = decs_dict[op]
            new_line = ""
            for key, value in decorator.items():
                new_line += f"{key}: *{value}*  "
            lines.insert(0, new_line)
            lines.insert(1, "")
    return lines


# signature processing - used to identify which methods are being processed for the docstring processing (method_name)
def signature_processing(app, what, name, obj, options, signature, return_annotation):
    global method_name
    method_name = name.split('.')[len(name.split('.'))-1]


# identify members to skip in the autosummary - used for microservices to ensure only the service ops are included
def skip_members(app, what, name, obj, skip, options):
    if name == "__init__":
        return True
    if what == "method":
        class_name = obj.__qualname__.split('.')[0]
        if class_name != "object":
            mod = obj.__module__
            if mod:
                repo = mod.split('.')[0]
                mod_name = repo.replace('-', '_')
                module = import_module(f"{mod_name}.{mod_name}")
                if hasattr(module, "setup"):
                    setup = getattr(module, "setup")
                else:
                    return None
                custom_ops = dict(
                    [[x.name, x] for x in ast.walk(ast.parse(inspect.getsource(setup))) if type(x).__name__ == 'FunctionDef']
                )
                svc_ops = []
                for op in custom_ops:
                    decs = custom_ops[op].decorator_list
                    for dec in decs:
                        kws = dec.keywords
                        if len(kws) == 3:
                            svc_ops.append(op)
                if name not in svc_ops:
                    return True


def setup(app):
    app.add_css_file('styles.css')
    app.connect("autodoc-process-docstring", extra_processing)
    app.connect("autodoc-process-signature", signature_processing)
    app.connect("autodoc-skip-member", skip_members)


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
    'sidebar_header': '#180075',
    'sidebar_link': '#180075',
    'narrow_sidebar_bg': '#180075',
    'narrow_sidebar_link': '#3DBCD8',
    'link': '#180075',
    'link_hover': '#A70B52',
    'show_powered_by': False,
    'head_font_family': "Source Sans Pro Bold",
    'font_family': "Source Sans Pro",
    'caption_font_family': "Source Sans Pro Italic",
    # 'pre_bg': '#3DBCD8',
    # 'note_bg': '#FFE4E1',
    'note_border': '#A70B52',
}

# -- Options for LaTeX output -------------------------------------------------

# The theme to use for LaTeX pages.  See the documentation for
# a list of builtin themes.
#
latex_theme = 'howto'

# other elements used in latex pdf generation
latex_elements = {
    'figure_align': 'H',
    'preamble': r'\usepackage{enumitem}\setlistdepth{99}\usepackage{charter}\usepackage[defaultsans]{lato}\usepackage{inconsolata}\setlength{\fboxsep}{6pt}',
    'makeindex': r'\usepackage[columns=1]{idxlayout}\makeindex',
    'atendofbody': r'\vspace*{\fill}\textit{HMD Labs Confidential – This document contains information that is confidential and proprietary. Neither this document nor the information herein may be reproduced, used, or disclosed to or for the benefit of any third party without the prior written consent of HMD Labs.}\pagebreak',
    'sphinxsetup': r'VerbatimColor={RGB}{235,236,240}, verbatimwithframe=false, noteBorderColor={RGB}{167,11,82}, InnerLinkColor={RGB}{24,0,117}, TitleColor={RGB}{24,0,117}, vmargin={0.75in,0.75in}'
}

latex_logo = f"./{html_static_path[0]}/NeuronSphereSwoosh.jpg"
