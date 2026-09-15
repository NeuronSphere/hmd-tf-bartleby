# Changelog

## 2026-09-15

### needs.json is exported by default

- feat: `conf.py` sets `needs_build_json = True`, so every build writes
  sphinx-needs' `needs.json` into the builder's output directory alongside the
  rendered document. sphinx-needs writes it only when asked, so a repository
  that declares requirements previously had to set the flag itself, or run a
  second build with different settings, to get the machine-readable copy of the
  data the first build already had in hand. The default is applied before the
  manifest's `config` block, so a repository can still turn it off with
  `"needs_build_json": false`.
- test: `Needs Data Is Exported By Default` runs the transform and checks that
  the exported file carries the requirement the fixture declares. That fixture
  is an orphaned page, `test/input_files1/docs/needs_fixture.rst` — needs are
  collected when a document is read, so the item reaches `needs.json` without
  entering the rendered document the PDF, Word and PowerPoint suites check. The
  templated `html` and `pdf` cases also expect `needs.json` now, which covers
  both builders' output directories for free.

## 2026-09-11

### The docker build could not resolve Sphinx 9

- fix: `hmd docker build` compiled `src/docker/requirements.in` into a lock using
  the *host* Python, and both nsenv and the `hmd-img-projectbuilder` build image
  are 3.11 while this image runs 3.13. `sphinx==9.1.0` requires 3.12, so the
  resolution was unsatisfiable and the build failed in 19 seconds without ever
  reaching Docker. The pins now live directly in `src/docker/requirements.txt`
  and no compile runs. The image is unchanged: `--upgrade-strategy eager`
  already upgraded past the lock's transitive pins, so the direct pins were the
  only part of that file that reached it. `make image-local` never ran the
  compile, which is why the upgrade cycle did not catch this.
- fix: the transform's own package is installed by an explicit
  `pip install /src/python/` in `src/docker/Dockerfile`, matching
  `Dockerfile.dev` and `Dockerfile.local`. `hmd-cli-docker` used to append that
  path to the file it generated for `install_local` repos, and it no longer
  generates one.

## 2026-09-05 — Word and PowerPoint

### A documentation build could hang forever

Found by the upgrade cycle's own test run, which spent **61 minutes** inside
`make html` before failing — and whose only visible symptom was a missing output
file.

- fix: `conf.py` fetched a logo given as a URL with `requests.get(...)` and **no
  timeout**, so an unresponsive host blocked the build indefinitely. The fetch
  is now bounded at `(5, 30)` and a failure is an error naming the URL and the
  reason. Being network-dependent, it was intermittent: the same suite passed
  12/12 an hour earlier.
- fix: the download opened the destination file *before* the request, so a
  failure left a zero-byte image behind that the build would then use as the
  logo. It is written beside it and moved into place only once complete.
- feat: `REQ_BRAND_007`, covered by a test that points the logo at `192.0.2.1`
  — TEST-NET-1, which RFC 5737 reserves and nothing routes — and requires the
  build to fail in under two minutes rather than wait.
- fix: the Robot suite could not see a failed transform. `docker-compose up`
  exits 0 however the container ended, so every case's `rc == 0` assertion was
  vacuous and the hour-long failure surfaced only as an absent file. It now runs
  with `--exit-code-from`.

### Package currency

The previous entry updated the *pinned* requirements, which is not the same as
updating the image. `pip install -r` only upgrades what the file names, so every
transitive dependency stayed at whatever the base image installed:
`pip list --outdated` on the built image reported **16** stale packages,
including `certifi` from January 2025, `urllib3`, and `pillow`.

- fix: `--upgrade-strategy eager`, so dependencies are upgraded too and not just
  the packages named in `requirements.in`. Sixteen stale packages became two,
  both capped by a constraint rather than missed: `docutils` stops at 0.22.4
  because Sphinx 9.1 requires `<0.23`, and `jsonschema-rs` at 0.52.1 because
  sphinx-needs 8.5.0 requires `<0.53.0`.
- fix: `pillow` is pinned. Nothing in the requirement graph referenced it — the
  base image installs it and Sphinx uses it for images — so nothing kept it
  current, and Pillow is where the image-parsing CVEs live. 11.1.0 → 12.3.0.
- fix: removed the deprecated `roman-numerals-py`, which was installed alongside
  its replacement `roman-numerals`. **Both install the same `roman_numerals`
  module**, so which one answered `import roman_numerals` depended on install
  order. Uninstalling the deprecated distribution deletes the shared module
  files out from under the current one — confirmed, it leaves
  `ModuleNotFoundError` — so the Dockerfiles remove and reinstall in one layer.
- fix: OS packages are upgraded within bookworm. `apt list --upgradable` in the
  published image reported **68**, including `bash`, `dpkg`, `base-files` and
  `ca-certificates` — the base image ships whatever its packages were the day it
  was built and nothing since.
- The runtime Python stays at **3.13.2**, which is the base image's. There is no
  `sphinxdoc/sphinx-latexpdf` tag beyond 8.2.3, so moving to 3.14 means building
  our own texlive base — the thing that base image exists to avoid. The
  throwaway download stage moved to `python:3.14-slim`, which affects nothing at
  runtime.

- feat: `docx` and `pptx` builders, converting the rendered documentation with
  pandoc 3.11. Sphinx has no writer for either and every community docx
  extension is abandoned — `docxbuilder` last released in 2020, and there is no
  pptx extension at all. Both outputs are named like the PDF and lifted to the
  top of the output directory. `HMD_DOC_REFERENCE_DOCX` and
  `HMD_DOC_REFERENCE_PPTX` name a document whose styles the output adopts.
  See NERD005.
- fix: the conversion reads an extracted document body, not the rendered page.
  pandoc converts a whole page, so the themed output put the sidebar, the search
  box and the `¶` heading permalinks into the Word document — and in PowerPoint
  the theme's own `<h1>` outranked the document title and took the first slide.
- fix: `<section>` wrappers are removed before conversion. Sphinx wraps every
  section in one, pandoc reads it as a Div, and a heading inside a Div starts no
  slide — so the entire document arrived on a single slide whatever
  `--slide-level` said. Both defects exited zero and produced plausible files;
  they were found by inspecting the documents, not by a build failing.
- feat: a requirements baseline for the transform, and `reqtrace` wired in as
  `make reqs` / `make reqs-check` / `make check`. Nineteen requirements across
  BUILD, BRAND, SEL and CONV; the Robot suite carries the IDs it verifies.
- feat: the Robot suite covers the copyright override and the two new builders —
  twelve cases, up from eight. `resources/OfficeChecks.py` reads the produced
  `.docx` and `.pptx` with nothing outside the standard library.
- fix: `meta-data/manifest.json` had `"name": "repo_name"` from a template. That
  is the document title and the requirement ID prefix, so this repository's own
  documents were titled "repo_name".


## 2026-09-05

Dependency upgrade cycle. Verified against the requirements-heavy docs in
`hmd-cli-bartleby` (122 sphinx-needs items) and a fixture exercising the
builders those docs do not: HTML, PDF, RevealJS, and PlantUML all build with
**zero warnings**, and the Robot suite passes 8/8 against the rebuilt image.

- feat: Sphinx 8.2.3 → **9.1.0**. The `sphinxdoc/sphinx-latexpdf` base image has
  no 9.x tag, so it stays at 8.2.3 and requirements upgrade Sphinx over it. Those
  two version numbers are meant to differ; the Dockerfiles say so.
- feat: sphinx-needs 6.3.0 → **8.5.0**, two majors. Nothing in the existing
  `req`/`spec`/`needtable` usage or the `needs_id_regex` and `needs_warnings`
  config broke; 8.x adds schema validation, which passes clean.
- feat: myst-parser 5.0.0 → 5.1.0, sphinxcontrib-confluencebuilder 3.0.0 → 3.2.0,
  `requests` pinned at 2.34.2 rather than floating.
- feat: PlantUML **1.2023.7 → 1.2026.7**, three years of releases, and now
  downloaded from its GitHub release rather than the SourceForge mirror the
  Makefile already described as "often slow and sometimes serves an HTML error
  page instead". The download is checksum-verified, so a truncated or
  substituted jar fails the build rather than surfacing at render time.
- fix: `make image-local` preferred the jar from the published image, which
  carries whatever PlantUML it was built with — so a version bump here would
  have been silently ignored locally. The cached jar is now checked against
  `PLANTUML_SHA256` and re-downloaded when it does not match.
- fix: every build emitted two warnings about `_static/SourceSansPro/OFL.txt`, a
  font licence that MyST parsed as a document. `_static` is excluded from source
  discovery; static assets still copy.
- fix: dropped `roman-numerals-py<4`. That distribution is deprecated in favour
  of `roman-numerals`, which is what Sphinx 9 depends on, so the cap constrained
  a package nothing was asking for.
- fix: dropped `when-changed==0.3.0`. A 2016 file-watcher that nothing in the
  repository referenced.
- feat: `make test` runs the Robot suite against a locally built image. Two
  things it needs were easy to lose: `--pythonpath`, because newer Robot
  Framework no longer adds the suite's directory to `sys.path` and the
  PDF-checking library lives in `test/resources`, and `TRANSFORM_IMAGE`, which
  the compose file now honours — previously the suite could only test the
  published image. The compose default also points at `neuronsphere` rather than
  the old `hmdlabs` path, and the obsolete `version:` key is gone.


## 2026-09-04

- feat: `HMD_DOC_COPYRIGHT` replaces the footer notice outright, and
  `HMD_DOC_AUTHOR` the author. The line was assembled as `<year>, <company>`,
  which allows "2026, GitLab Inc." and nothing else — no notice without a year,
  no "All rights reserved", no third-party attribution. `copyright` and `author`
  in a repository's manifest config also work, and are the better home for a
  permanent notice.
- fix: `HTML_DEFAULT_LOGO` did nothing. It and `PDF_DEFAULT_LOGO` were assigned
  to the same variable, PDF second, so the HTML sidebar logo was whatever the PDF
  variable said. They are separate settings now.
- fix: two logos rendered when a repository set `html_logo`. Sphinx and the theme
  have separate logo mechanisms and both were live: this transform always set
  `html_theme_options["logo"]`, and a repository's `html_logo` added Sphinx's own
  sidebar logo block on top of it, so the output stacked the repository's mark
  above the NeuronSphere swoosh. Setting `html_logo` now replaces the logo, and
  the build log records which one was kept.
- docs: NERD004 records these as requirements; the README documents the branding
  variables.


## 2026-08-31

- fix: fail the transform when Sphinx fails. The exit code was captured and only
  logged, so a document that did not compile produced a container that exited 0
  and every caller reported a broken build as a success. The failure is raised
  after the logs and any partial output are copied out, and names the log files.
- feat: write Sphinx warnings and errors to `logs/<builder>-warnings.log` via
  `SPHINXOPTS -w`, preserving any `SPHINXOPTS` the caller set. The combined log is
  mostly progress and `latexmk` output; the lines that explain a broken document
  were buried in it.
- feat: copy LaTeX's own log to `logs/<builder>-latex-*.log` after a PDF build,
  instead of leaving it in the `latex/` build tree beside megabytes of assets.
- feat: `make image-local` builds the image from the working tree — no network, no
  private index — for use with `bartleby --image hmd-tf-bartleby:local`. Adds
  `src/docker/Dockerfile.dev`, which takes `plantuml.jar` from the build context
  and installs the transform package from source. `Dockerfile.local` is unchanged
  because the HMD docker build depends on its context shape.
- fix: `curl -f` with retries and an archive check on the `plantuml.jar` download.
  Without `-f`, a SourceForge error page was written to `plantuml.jar` and the
  build carried on with a jar that was HTML.
- docs: NERD003 records these as requirements; README documents the local loop and
  the logs.


## 2026-02-26

- feat: upgrade Sphinx 7.1.2 to 8.2.3 and all documentation dependencies to latest stable
- feat: align Dockerfile.local with production Dockerfile (base image, plantuml, python3.11-dev)

## 2024-07-19

- fix: pins sphinx

## 2024-04-10

- fix: bumps version

## 2024-03-31

- feat: changed mode of makefile

## 2024-03-28

- fix: makes Makefile executable

## 2024-03-07

- fix: fixes copytree with symlinks

## 2023-11-01

- feat: adds confluence builder

## 2023-10-31

- feat: adds dynamic root docs

## 2023-10-27

- fix: fixes using revealjs

## 2023-09-14

- fix: removes revealjs from conf

## 2023-09-13

- fix: pins hmd-graphql
- fix: updates reqs.txt
- feat: adds custom doc title

## 2023-07-20

- feat: updated plantuml max image size env var

## 2023-07-02

- feat: updated plantUML dependency in dockerfile

## 2023-03-15

- fix: removes blank pages in pdf
- feat: adds sphinx needs extension

## 2023-03-09

- fix: fixes issue with timestamp in filename
- fix: copies pdf to target/bartleby/
- test: fixes pdf filename check

## 2023-03-08

- feat: allows overriding logo images
- test: adds robot tests for confidentiality stmnt
- test: converts robot tests to run with Bender

## 2023-03-03

- fix: builds docker from local src
- fix: updates hmd-cli-tools version
- feat: adds CONFIDENTIALITY_STATEMENT

## 2022-11-28

- fix: handles Makefile in prj root
- feat: adds copied files to gitignore
- feat: handles mounting prj root for README includes

## 2022-09-29

- fix: exclude full autosummary of imported classes
- fix: docstring processing and autodoc parsing

## 2022-09-27

- fix: dockerfile copy
- fix: removes escrow code and casts autodoc to bool

## 2022-07-28

- feat: adds consolidate_repo func for escrow transforms

## 2022-07-19

- feat: updates docstring handling and pdf format

## 2022-07-15

- feat: updates conf to add service op decorators to autosummary of custom ops

## 2022-03-16

- fix: corrects error when autodoc is false

## 2022-03-11

- fix: updates entrypoint to cmd

## 2022-03-09

- feat: adds support to generate images from puml, updates doc theme formatting

## 2022-03-04

- feat: pipes sphinx logs to a log file
- feat: adds support for gather mode
