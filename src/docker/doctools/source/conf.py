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
import json
from urllib.parse import unquote
import datetime
from importlib import import_module
import inspect
import ast
import requests

sys.path.insert(0, os.path.abspath("../packages"))

# -- Transform Context -------------------------------------------------------

transform_instance_context = json.loads(os.environ.get("TRANSFORM_INSTANCE_CONTEXT"))
print(transform_instance_context)

# -- Project information -----------------------------------------------------
company_name_acronym = os.environ.get("HMD_DOC_COMPANY_NAME", "HMD Labs")
repo_name = os.environ.get("HMD_DOC_REPO_NAME")
repo_version = os.environ.get("HMD_DOC_REPO_VERSION")
if len(repo_name.split(",")) == 1:
    project = "{}".format(repo_name)
    release = repo_version
else:
    project = f"{repo_name}"
    release = f"{os.environ.get('HMD_CUSTOMER_CODE', 'HMD')}-{os.environ.get('HMD_DID', 'aaa')}"

project = os.environ.get("DOCUMENT_TITLE", project)
copyright = "{}, {}".format(datetime.date.today().year, company_name_acronym)
author = "{}".format(company_name_acronym)

# -- General configuration ---------------------------------------------------

root_doc = transform_instance_context.get("root_doc", "index")

# Add any Sphinx extension module names here, as strings. They can be
# extensions coming with Sphinx (named 'sphinx.ext.*') or your custom
# ones.
# TODO: add option to extend this list, along with requirements.txt
extensions = [
    "sphinx_revealjs",
    "sphinx_copybutton",
    "sphinxcontrib.plantuml",
    "sphinxcontrib.confluencebuilder",
    "sphinxcontrib.datatemplates",
    "sphinx.ext.autodoc",
    "sphinx.ext.autosummary",
    "nbsphinx",
    "myst_parser",
    "sphinx_needs",
]

source_suffix = {
    ".rst": "restructuredtext",
    ".txt": "markdown",
    ".md": "markdown",
}

autodoc_default_options = {
    "members": True,
    "undoc-members": True,
    "private-members": False,
    "imported-members": False,
    "show_inheritance": False,
    "exclude-members": "__init__",
    "member-order": "bysource",
}

# autodoc check for signatures within source code
autodoc_docstring_signature = True

autosummary_generate = True

nbsphinx_requirejs_path = (
    "https://cdnjs.cloudflare.com/ajax/libs/require.js/2.3.6/require.min.js"
)


# docstring processing
def extra_processing(app, what, name, obj, options, lines):
    repo = name.split(".")[0]
    mod_name = repo.replace("-", "_")
    module = import_module(f"{mod_name}.{mod_name}")
    if hasattr(module, "setup"):
        setup = getattr(module, "setup")
    else:
        return lines
    custom_ops = dict(
        [
            [x.name, x]
            for x in ast.walk(ast.parse(inspect.getsource(setup)))
            if type(x).__name__ == "FunctionDef"
        ]
    )
    for op in custom_ops:
        decs = custom_ops[op].decorator_list
        decs_dict = {}
        for dec in decs:
            kws = dec.keywords
            kw_dict = {}
            for kw in kws:
                if kw.arg == "rest_path":
                    kw_dict.update({f"**{kw.arg}**": ast.parse(kw.value).value})
                elif kw.arg == "rest_methods":
                    try:
                        kw_dict.update(
                            {f"**{kw.arg}**": ast.parse(kw.value).elts[0].value}
                        )
                    except Exception as e:
                        pass
                elif kw.arg == "args":
                    try:
                        kw_dict.update(
                            {
                                f"**{kw.arg}**": {
                                    ast.parse(kw.value)
                                    .keys[0]
                                    .value: ast.parse(kw.value)
                                    .values[0]
                                    .value
                                }
                            }
                        )
                    except Exception as e:
                        pass
            decs_dict.update({op: kw_dict})
        if op == method_name and len(decs_dict.get(op, {})) > 0:
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
    method_name = name.split(".")[len(name.split(".")) - 1]


# identify members to skip in the autosummary - used for microservices to ensure only the service ops are included
def skip_members(app, what, name, obj, skip, options):
    if name == "__init__":
        return True
    if what == "method":
        class_name = obj.__qualname__.split(".")[0]
        if class_name != "object":
            mod = obj.__module__
            if mod:
                repo = mod.split(".")[0].replace("_", "-")
                print(repo)
                if repo == repo_name:
                    mod_name = repo.replace("-", "_")
                    module = import_module(f"{mod_name}.{mod_name}")
                    if hasattr(module, "setup"):
                        setup = getattr(module, "setup")
                    else:
                        return None
                    custom_ops = dict(
                        [
                            [x.name, x]
                            for x in ast.walk(ast.parse(inspect.getsource(setup)))
                            if type(x).__name__ == "FunctionDef"
                        ]
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
    app.add_css_file("styles.css")
    app.connect("autodoc-process-docstring", extra_processing)
    app.connect("autodoc-process-signature", signature_processing)
    app.connect("autodoc-skip-member", skip_members)


# Add any paths that contain templates here, relative to this directory.
templates_path = ["_templates"]

# List of patterns, relative to source directory, that match files and
# directories to ignore when looking for source files.
# This pattern also affects html_static_path and html_extra_path.
exclude_patterns = []

# path to jar file used for generating puml diagrams
plantuml = "java -jar /usr/local/bin/plantuml.jar"

# -- Options for HTML output -------------------------------------------------

# The theme to use for HTML and HTML Help pages.  See the documentation for
# a list of builtin themes.
#
# html_theme = "alabaster"

# Add any paths that contain custom static files (such as style sheets) here,
# relative to this directory. They are copied after the builtin static files,
# so a file named "default.css" will overwrite the builtin "default.css".
html_static_path = ["_static"]
# html_logo = f"./{html_static_path[0]}/Neuron_Sphere_Symbol_Color2.png"

default_logo = os.environ.get(
    "DEFAULT_LOGO", f"./{html_static_path[0]}/NeuronSphereSwoosh.jpg"
)

# In case empty string is passed
if not default_logo:
    default_logo = f"./{html_static_path[0]}/NeuronSphereSwoosh.jpg"

default_html_logo = os.environ.get("HTML_DEFAULT_LOGO", default_logo)

default_html_logo = os.environ.get("PDF_DEFAULT_LOGO", default_logo)

if default_html_logo.startswith("http"):
    filename = default_html_logo.split("?")[0].split("/")[-1]
    with open(f"./{html_static_path[0]}/{filename}", "wb") as handler:
        resp = requests.get(default_html_logo, stream=True)

        if not resp.ok:
            raise Exception(f"Cannot download PDF_DEFAULT_LOGO {default_html_logo}")

        for chunk in resp.iter_content(1024):
            if not chunk:
                break

            handler.write(chunk)

    default_html_logo = filename
else:
    default_html_logo = default_html_logo.removeprefix(f"./{html_static_path[0]}")

html_theme_options = {
    "logo": default_html_logo,
    "logo_name": True,
    "page_width": "1100px",
    "sidebar_width": "270px",
    "sidebar_header": "#180075",
    "sidebar_link": "#180075",
    "narrow_sidebar_bg": "#180075",
    "narrow_sidebar_link": "#3DBCD8",
    "link": "#180075",
    "link_hover": "#A70B52",
    "show_powered_by": False,
    "head_font_family": "Source Sans Pro Bold",
    "font_family": "Source Sans Pro",
    "caption_font_family": "Source Sans Pro Italic",
    # 'pre_bg': '#3DBCD8',
    # 'note_bg': '#FFE4E1',
    "note_border": "#A70B52",
}

# -- Options for LaTeX output -------------------------------------------------

# The theme to use for LaTeX pages.  See the documentation for
# a list of builtin themes.
#
latex_theme = "howto"

# other elements used in latex pdf generation
latex_elements = {
    "extraclassoptions": "openany,oneside",
    "figure_align": "H",
    "preamble": r"\usepackage{enumitem}\setlistdepth{99}\usepackage{charter}\usepackage[defaultsans]{lato}\usepackage{inconsolata}\setlength{\fboxsep}{6pt}",
    "makeindex": r"\usepackage[columns=1]{idxlayout}\makeindex",
    "sphinxsetup": r"VerbatimColor={RGB}{235,236,240}, verbatimwithframe=false, noteBorderColor={RGB}{167,11,82}, InnerLinkColor={RGB}{24,0,117}, TitleColor={RGB}{24,0,117}, vmargin={0.75in,0.75in}",
}

print(os.environ.get("CONFIDENTIALITY_STATEMENT", None))
if os.environ.get("CONFIDENTIALITY_STATEMENT", None) is not None:
    latex_elements["atendofbody"] = (
        r"\vspace*{\fill}\textit{"
        + os.environ.get("CONFIDENTIALITY_STATEMENT")
        + r"}\pagebreak"
    )


latex_logo = os.environ.get("PDF_DEFAULT_LOGO", default_logo)

if latex_logo.startswith("http"):
    filename = unquote(latex_logo).split("?")[0].split("/")[-1]
    with open(f"./{html_static_path[0]}/{filename}", "wb") as handler:
        resp = requests.get(latex_logo, stream=True)

        if not resp.ok:
            raise Exception(f"Cannot download PDF_DEFAULT_LOGO {latex_logo}")

        for chunk in resp.iter_content(1024):
            if not chunk:
                break

            handler.write(chunk)

    latex_logo = f"./{html_static_path[0]}/{filename}"

# set document naming
doc_name = os.environ.get("DOCUMENT_TITLE", f"{repo_name}-{repo_version}")
if not os.environ.get("NO_TIMESTAMP_TITLE"):
    doc_name = doc_name + datetime.datetime.now().strftime("%Y-%m-%d_%H_%M_%S")
latex_documents = [("index", f"{doc_name}.tex", project, author, "manual")]

# -- Options for RevealJS output -------------------------------------------------

revealjs_js_files = []
revealjs_css_files = []
revealjs_static_path = ["_static"]
revealjs_script_conf = '{"controls": true}'

extra_config = transform_instance_context.get("config", {})

for key, value in extra_config.items():
    globals()[key] = value
