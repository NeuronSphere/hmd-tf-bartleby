# syntax = docker/dockerfile:1.0-experimental

FROM sphinxdoc/sphinx-latexpdf
COPY doctools /hmd_transform/doctools
COPY requirements.txt .

RUN --mount=type=secret,id=pipconfig,dst=/etc/pip.conf \
    pip install -r requirements.txt

ENV TRANSFORM_INSTANCE_CONTEXT default
ENV TRANSFORM_NID default

WORKDIR /app
COPY entrypoint.py .

ENTRYPOINT [ "python", "entrypoint.py" ]