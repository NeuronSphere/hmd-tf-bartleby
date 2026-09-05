# hmd-tf-bartleby

Runs the document generation transform.

This is the runtime half of Bartleby: a container image with Sphinx, LaTeX, and
PlantUML that renders a repository's `docs/` to HTML, PDF, RevealJS slides, or
PlantUML images. The CLI that drives it lives in
[hmd-cli-bartleby](https://github.com/NeuronSphere/hmd-cli-bartleby).

## Local development

Build the image from the working tree and run the CLI against it:

```bash
make image-local          # builds hmd-tf-bartleby:local
cd ../some-docs-repo
bartleby --image hmd-tf-bartleby:local html
```

`make image-local` needs no private index credentials: it installs the
transform's Python package from source, and takes `plantuml.jar` from an image
already on this machine when that copy matches the pinned version — otherwise it
downloads and checksum-verifies it. A code-only change rebuilds in seconds.
`make help` lists the rest of the targets; `make smoke` reports the Sphinx and
PlantUML the built image will use.

### Tests

```bash
make test                      # Robot suite against hmd-tf-bartleby:local
make test TAG=other            # or another local tag
```

The suite renders through the container and checks the results, including
reading the produced PDFs for the confidentiality statement and the cover logo.
It needs Docker and Compose; `ROBOT` defaults to `uvx`, so its Python
dependencies need not be installed globally.

Worth knowing what it does *not* cover: the Confluence builder, and the branding
environment variables. Renders of a real repository are the check for those —
`../hmd-cli-bartleby` is a good target, since its documentation is dense with
sphinx-needs items.

## Interface

The CLI passes the transform its instructions through the environment and two
bind mounts. `docs/transforms.rst` documents the contract; the parts worth knowing
here:

| Path | Direction | Contents |
|------|-----------|----------|
| `/hmd_transform/input` | in | The repository being documented |
| `/hmd_transform/output` | out | Rendered documents, plus `logs/` |
| `/hmd_transform/global_styles` | in, optional | `$HMD_HOME/bartleby/styles`, read-only |

### Branding

| Variable | Effect |
|----------|--------|
| `HMD_DOC_COPYRIGHT` | The whole footer notice. Defaults to `<year>, <company>` |
| `HMD_DOC_COMPANY_NAME` | The company in that default, and the default author |
| `HMD_DOC_AUTHOR` | The author, independently of the company |
| `HTML_DEFAULT_LOGO` | The HTML sidebar logo |
| `PDF_DEFAULT_LOGO` | The PDF cover image |
| `DEFAULT_LOGO` | Fallback for both |

A repository can set `copyright`, `author`, and `html_logo` in its manifest
config instead, which is the better home for a permanent notice — per-repo config
is applied to Sphinx settings after `conf.py` runs, so it wins.

Setting `html_logo` replaces the logo rather than adding to it: the theme's own
default steps aside, and the build log says which logo it kept. Note the footer
renders `©` immediately before your string, so include any spacing you want.

### Logs

Everything needed to diagnose a build lands in `/hmd_transform/output/logs/`,
which is `target/bartleby/logs/` on the host:

| File | Contents |
|------|----------|
| `<builder>.log` | Everything Sphinx and, for PDF, `latexmk` printed |
| `<builder>-warnings.log` | Only Sphinx's warnings and errors — start here |
| `<builder>-latex-*.log` | LaTeX's own log for a PDF build |

A build that fails exits non-zero and names those files. Set `SPHINXOPTS` to pass
extra options to `sphinx-build`; the warnings file is appended to whatever you
set, not instead of it.

See `docs/proposals/NERD003_Diagnosable_Build_Failures.rst` for why those exist.
