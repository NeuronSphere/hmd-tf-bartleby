# Stage 1: Download build artifacts in a lightweight throwaway image
FROM python:3.14-slim AS deps

# PlantUML comes from its GitHub release rather than the SourceForge mirror,
# which is slow and has been known to serve an HTML error page in place of the
# jar. The checksum is what makes that safe to rely on: a truncated or
# substituted download fails the build here instead of at render time.
ARG PLANTUML_VERSION=1.2026.7
ARG PLANTUML_SHA256=33aa7ed0ca843e300690230d09268e1f526fdde7e86fecdfa39fb80412cafcde

RUN apt-get update && \
    apt-get install -y --no-install-recommends curl && \
    curl -fL --retry 5 --retry-delay 2 --retry-all-errors --connect-timeout 20 \
      "https://github.com/plantuml/plantuml/releases/download/v${PLANTUML_VERSION}/plantuml-${PLANTUML_VERSION}.jar" \
      -o /plantuml.jar && \
    echo "${PLANTUML_SHA256}  /plantuml.jar" | sha256sum -c - && \
    rm -rf /var/lib/apt/lists/*

# Pandoc converts the rendered documentation to Word and PowerPoint, which
# Sphinx has no writer for. The .deb is per-architecture, so both checksums are
# pinned and the wrong one fails the build rather than installing silently.
ARG PANDOC_VERSION=3.11
ARG PANDOC_SHA256_AMD64=89d4c9d97818c62a97157f0072844e4602c6cee795bf84abd1aee7273abcda99
ARG PANDOC_SHA256_ARM64=d03e1be90fa510aaddc9b1e17f3e4615de0ab8a0aa7e7553502a3c9701887730

RUN arch="$(dpkg --print-architecture)" && \
    case "$arch" in \
      amd64) sha="${PANDOC_SHA256_AMD64}" ;; \
      arm64) sha="${PANDOC_SHA256_ARM64}" ;; \
      *) echo "no pinned pandoc checksum for $arch" >&2; exit 1 ;; \
    esac && \
    curl -fL --retry 5 --retry-delay 2 --retry-all-errors --connect-timeout 20 \
      "https://github.com/jgm/pandoc/releases/download/${PANDOC_VERSION}/pandoc-${PANDOC_VERSION}-1-${arch}.deb" \
      -o /pandoc.deb && \
    echo "${sha}  /pandoc.deb" | sha256sum -c -

# Stage 2: Runtime image with full texlive for broad PDF support
#
# The tag tracks the newest sphinx-latexpdf image, which is 8.2.3; requirements
# then upgrade Sphinx over it. Those two numbers are meant to differ — do not
# "fix" the mismatch by pinning Sphinx back to the base image's version.
FROM sphinxdoc/sphinx-latexpdf:8.2.3

# The base image ships whatever its packages were on the day it was built, and
# nothing since. `apt list --upgradable` in the published image reported 68,
# including bash, dpkg, base-files and ca-certificates — the OS half of the same
# staleness the eager pip upgrade fixes. Upgrading here stays inside bookworm:
# point releases and security updates, not a distro bump.
RUN apt-get update && \
    apt-get upgrade -y --no-install-recommends && \
    apt-get install -y --no-install-recommends default-jre-headless && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

COPY --from=deps /plantuml.jar /usr/local/bin/plantuml.jar
COPY --from=deps /pandoc.deb /tmp/pandoc.deb
RUN dpkg -i /tmp/pandoc.deb && rm /tmp/pandoc.deb


COPY src/docker/doctools /hmd_transform/doctools
COPY meta-data /meta-data
COPY src/python /src/python
COPY src/docker/requirements.txt .

# --upgrade-strategy eager upgrades the dependencies too, not just the pinned
# packages. Without it, pip leaves everything the base image installed at
# whatever version that was: a `pip list --outdated` on the built image showed
# 16 stale packages, including certifi, urllib3 and pillow. Constraints still
# apply — docutils stops at the highest release Sphinx allows.
RUN --mount=type=secret,id=pipconfig,dst=/etc/pip.conf \
    pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir --upgrade --upgrade-strategy eager -r requirements.txt

# roman-numerals-py is the deprecated name for roman-numerals, and both install
# the same `roman_numerals` module. Both end up present: the base image
# installed the old one, Sphinx 9 requires the new one, and whichever landed
# last owns the files. Uninstalling the deprecated distribution therefore
# deletes the module out from under the current one — verified, it leaves
# ModuleNotFoundError — so it is reinstalled in the same layer.
RUN pip uninstall -y roman-numerals-py && \
    pip install --no-cache-dir --force-reinstall --no-deps roman-numerals

# The transform's own package. hmd-cli-docker appended `/src/python/` to the
# requirements file it generated for install_local repos; with that compile step
# gone it is installed explicitly here, as Dockerfile.dev and Dockerfile.local
# already do.
RUN pip install --no-cache-dir /src/python/


ENV TRANSFORM_INSTANCE_CONTEXT="{\"shell\": \"default\"}"
ENV NID_CONTEXT=default
ENV PLANTUML_LIMIT_SIZE=8192

WORKDIR /app
COPY src/docker/entrypoint.py .
COPY src/docker/entry_puml.py .

CMD [ "python", "entrypoint.py" ]
