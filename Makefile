# Local development for the Bartleby transform image.
#
# The published image is built by the HMD build tooling, which installs the
# transform's Python package from the private index. These targets build the same
# image from the working tree instead — the source you are editing, no private
# index, no network — so a change to the entrypoint or the doctools can be tried
# without cutting a release.
#
#     make image-local
#     cd ../some-docs-repo && bartleby --image hmd-tf-bartleby:local html
#
# After editing src/python or src/docker, re-run `make image-local`; the pip layer
# is cached, so a code-only change rebuilds in seconds.

IMAGE     ?= hmd-tf-bartleby
TAG       ?= local
PUBLISHED ?= ghcr.io/neuronsphere/hmd-tf-bartleby:stable

CONTEXT := target/docker-context
JAR     := target/plantuml.jar

# Kept in step with the ARG default in src/docker/Dockerfile. Only used when
# neither the published image nor a Homebrew copy can supply the jar.
# reqtrace generates and checks the requirements traceability matrix. Install it
# with `brew install neuronsphere/tap/reqtrace`, or run it straight from source:
#   make reqs REQTRACE="go run github.com/neuronsphere/hmd-cli-bartleby/src/go/reqtrace/cmd/reqtrace@latest"
REQTRACE ?= reqtrace

PLANTUML_VERSION ?= 1.2026.7
PLANTUML_SHA256  ?= 33aa7ed0ca843e300690230d09268e1f526fdde7e86fecdfa39fb80412cafcde

# shasum on macOS, sha256sum on most Linux.
SHA256 := $(shell command -v shasum > /dev/null 2>&1 && echo "shasum -a 256" || echo sha256sum)

.PHONY: help image-local context jar jar-verify smoke test reqs reqs-check check clean

## help: show this help
help:
	@grep -E '^## ' $(MAKEFILE_LIST) | sed 's/^## /  /'

## jar: cache plantuml.jar locally, preferring a copy already on this machine
jar: $(JAR)

# The jar is checksum-verified against PLANTUML_SHA256, which is what makes the
# fast path safe: pulling it out of a local image beats re-downloading 30 MB,
# but the published image carries whatever jar it was built with — so when that
# is a different version, the checksum fails and we fall through to the
# download instead of quietly building against the wrong PlantUML.
$(JAR):
	@mkdir -p $(dir $(JAR))
	@if docker image inspect $(PUBLISHED) > /dev/null 2>&1; then \
		echo "trying plantuml.jar from $(PUBLISHED)"; \
		cid=$$(docker create $(PUBLISHED)) && \
		docker cp $$cid:/usr/local/bin/plantuml.jar $(JAR) 2>/dev/null; \
		docker rm $$cid > /dev/null; \
	fi
	@if ! $(MAKE) -s jar-verify 2>/dev/null; then \
		echo "downloading plantuml.jar $(PLANTUML_VERSION)"; \
		curl -fL --retry 5 --retry-delay 2 --retry-all-errors --connect-timeout 20 \
		  "https://github.com/plantuml/plantuml/releases/download/v$(PLANTUML_VERSION)/plantuml-$(PLANTUML_VERSION).jar" \
		  -o $(JAR); \
		$(MAKE) -s jar-verify; \
	fi
	@echo "plantuml.jar $(PLANTUML_VERSION) ok"

## jar-verify: fail unless the cached jar matches PLANTUML_SHA256
jar-verify:
	@test -f $(JAR) || { echo "no $(JAR)"; exit 1; }
	@actual=$$($(SHA256) $(JAR) | cut -d" " -f1); \
	if [ "$$actual" != "$(PLANTUML_SHA256)" ]; then \
		echo "$(JAR) is not PlantUML $(PLANTUML_VERSION) (sha256 $$actual)"; \
		exit 1; \
	fi

## context: stage the flattened build context under target/docker-context
context: $(JAR)
	@rm -rf $(CONTEXT)
	@mkdir -p $(CONTEXT)
	cp -R src/docker/doctools $(CONTEXT)/doctools
	cp -R meta-data $(CONTEXT)/meta-data
	cp -R src/python $(CONTEXT)/python
	cp src/docker/entrypoint.py src/docker/entry_puml.py $(CONTEXT)/
	cp src/docker/Dockerfile.dev $(CONTEXT)/Dockerfile
	cp $(JAR) $(CONTEXT)/plantuml.jar
	@# The published requirements pin the transform's own package from the private
	@# index. Locally the package is installed from source instead, so that pin is
	@# dropped and no index credentials are needed.
	grep -v '^hmd-tf-bartleby' src/docker/requirements.in > $(CONTEXT)/requirements.txt
	@echo "staged $(CONTEXT) from the working tree"

## image-local: build $(IMAGE):$(TAG) from the working tree
image-local: context
	@# Dockerfile.dev deliberately avoids --mount=type=secret so this works with
	@# the classic builder too — BuildKit and buildx are not installed everywhere.
	cd $(CONTEXT) && docker build -t $(IMAGE):$(TAG) .
	@echo
	@echo "Built $(IMAGE):$(TAG). Use it with:"
	@echo "    bartleby --image $(IMAGE):$(TAG) html"

## test: run the Robot suite against $(IMAGE):$(TAG)
#
# Two things the suite needs that are easy to lose: --pythonpath, because newer
# Robot Framework no longer puts the suite's own directory on sys.path and the
# PDF-checking library lives in ./resources, and TRANSFORM_IMAGE, without which
# it tests the published image rather than the one you just built.
#
# ROBOT defaults to uvx so the suite's dependencies (PyMuPDF for reading the
# rendered PDFs) need not be installed globally. Override it to use your own:
#   make test ROBOT="python3 -m robot"
ROBOT ?= uvx --from robotframework --with pymupdf --with pyyaml robot

test:
	cd test && HMD_REPO_PATH="$$PWD" VERSION=$(TAG) TRANSFORM_IMAGE=$(IMAGE):$(TAG) \
	  $(ROBOT) --pythonpath . --outputdir results transform_run.robot

## reqs: regenerate docs/requirements/traceability.rst from the requirements and test annotations
reqs:
	$(REQTRACE) -repo $(CURDIR)

## reqs-check: fail if traceability has a gap or the generated matrix is stale
reqs-check:
	$(REQTRACE) -repo $(CURDIR) -check

## check: traceability — what CI can run without Docker
#
# The tests need Docker because they render through the container, so they are
# not part of this. `make check` is the part that holds anywhere.
check: reqs-check

## smoke: check the image runs and report the Sphinx and PlantUML it will use
smoke:
	docker run --rm --entrypoint sphinx-build $(IMAGE):$(TAG) --version
	docker run --rm --entrypoint java $(IMAGE):$(TAG) -jar /usr/local/bin/plantuml.jar -version | head -2

## clean: remove the staged context and the cached jar
clean:
	rm -rf $(CONTEXT) $(JAR)
