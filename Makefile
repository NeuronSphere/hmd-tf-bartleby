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

.PHONY: help image-local context jar smoke clean

## help: show this help
help:
	@grep -E '^## ' $(MAKEFILE_LIST) | sed 's/^## /  /'

## jar: cache plantuml.jar locally, preferring a copy already on this machine
jar: $(JAR)

# The published image carries the exact jar the released image uses, and pulling
# it out of a local image beats re-downloading 11 MB from a mirror that is often
# slow and sometimes serves an HTML error page instead.
$(JAR):
	@mkdir -p $(dir $(JAR))
	@if docker image inspect $(PUBLISHED) > /dev/null 2>&1; then \
		echo "extracting plantuml.jar from $(PUBLISHED)"; \
		cid=$$(docker create $(PUBLISHED)) && \
		docker cp $$cid:/usr/local/bin/plantuml.jar $(JAR) && \
		docker rm $$cid > /dev/null; \
	elif [ -f /opt/homebrew/opt/plantuml/libexec/plantuml.jar ]; then \
		echo "using the Homebrew plantuml.jar"; \
		cp /opt/homebrew/opt/plantuml/libexec/plantuml.jar $(JAR); \
	else \
		echo "downloading plantuml.jar"; \
		curl -fL --retry 5 --retry-delay 2 --retry-all-errors --connect-timeout 20 \
		  "https://sourceforge.net/projects/plantuml/files/1.2023.7/plantuml.1.2023.7.jar/download" \
		  -o $(JAR); \
	fi
	@unzip -t $(JAR) > /dev/null && echo "plantuml.jar ok"

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

## smoke: check the image runs and report the Sphinx and PlantUML it will use
smoke:
	docker run --rm --entrypoint sphinx-build $(IMAGE):$(TAG) --version
	docker run --rm --entrypoint java $(IMAGE):$(TAG) -jar /usr/local/bin/plantuml.jar -version | head -2

## clean: remove the staged context and the cached jar
clean:
	rm -rf $(CONTEXT) $(JAR)
