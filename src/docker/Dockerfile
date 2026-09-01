# Stage 1: Download build artifacts in a lightweight throwaway image
FROM python:3.13-slim AS deps

RUN apt-get update && \
    apt-get install -y --no-install-recommends curl unzip && \
    curl -fL --retry 5 --retry-delay 2 --retry-all-errors --connect-timeout 20 \
      "https://sourceforge.net/projects/plantuml/files/1.2023.7/plantuml.1.2023.7.jar/download" \
      -o /plantuml.jar && \
    unzip -t /plantuml.jar > /dev/null && \
    rm -rf /var/lib/apt/lists/*

# Stage 2: Runtime image with full texlive for broad PDF support
FROM sphinxdoc/sphinx-latexpdf:8.2.3

RUN apt-get update && \
    apt-get install -y --no-install-recommends default-jre-headless && \
    rm -rf /var/lib/apt/lists/*

COPY --from=deps /plantuml.jar /usr/local/bin/plantuml.jar

COPY src/docker/doctools /hmd_transform/doctools
COPY meta-data /meta-data
COPY src/python /src/python
COPY src/docker/requirements.txt .

RUN --mount=type=secret,id=pipconfig,dst=/etc/pip.conf \
    pip install --no-cache-dir -r requirements.txt

ENV TRANSFORM_INSTANCE_CONTEXT="{\"shell\": \"default\"}"
ENV NID_CONTEXT=default
ENV PLANTUML_LIMIT_SIZE=8192

WORKDIR /app
COPY src/docker/entrypoint.py .
COPY src/docker/entry_puml.py .

CMD [ "python", "entrypoint.py" ]
