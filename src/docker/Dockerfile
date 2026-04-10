FROM sphinxdoc/sphinx-latexpdf:8.2.3

COPY src/docker/doctools /hmd_transform/doctools

RUN apt-get update && \
    apt-get install -y --no-install-recommends curl default-jre-headless && \
    curl -L "https://sourceforge.net/projects/plantuml/files/1.2023.7/plantuml.1.2023.7.jar/download" -o /usr/local/bin/plantuml.jar && \
    apt-get purge -y curl && \
    apt-get autoremove -y && \
    rm -rf /var/lib/apt/lists/*

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
