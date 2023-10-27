# syntax = docker/dockerfile:1.0-experimental

FROM sphinxdoc/sphinx-latexpdf:7.1.2
COPY src/docker/doctools /hmd_transform/doctools
COPY src/docker/requirements.txt .

RUN apt-get update && apt install -y curl
RUN curl -L "https://sourceforge.net/projects/plantuml/files/1.2023.7/plantuml.1.2023.7.jar/download" -o /usr/local/bin/plantuml.jar

RUN apt install -y default-jre libpq-dev python3.11-dev postgresql gcc

COPY meta-data /meta-data
COPY src/python /src/python

RUN pip install cython
RUN --mount=type=secret,id=pipconfig,dst=/etc/pip.conf \
    pip install -r requirements.txt

ENV TRANSFORM_INSTANCE_CONTEXT {\"shell\": \"default\"}
ENV NID_CONTEXT default
ENV PLANTUML_LIMIT_SIZE 8192

WORKDIR /app
COPY src/docker/entrypoint.py .
COPY src/docker/entry_puml.py .

CMD [ "python", "entrypoint.py" ]