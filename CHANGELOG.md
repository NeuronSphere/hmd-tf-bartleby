# Changelog

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
