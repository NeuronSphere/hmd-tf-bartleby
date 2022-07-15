# syntax = docker/dockerfile:1.0-experimental

FROM sphinxdoc/sphinx-latexpdf
COPY doctools /hmd_transform/doctools
COPY requirements.txt .

RUN apt-get update && apt install -y curl
RUN curl -L "https://sourceforge.net/projects/plantuml/files/1.2021.14/plantuml.1.2021.14.jar/download" -o /usr/local/bin/plantuml.jar

RUN apt install -y default-jre libpq-dev python3-dev postgresql gcc

RUN --mount=type=secret,id=pipconfig,dst=/etc/pip.conf \
    pip install -r requirements.txt

ENV TRANSFORM_INSTANCE_CONTEXT {\"shell\": \"default\"}
ENV NID_CONTEXT default

WORKDIR /app
COPY entrypoint.py .
COPY entry_puml.py .

CMD [ "python", "entrypoint.py" ]