# Changelog

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
