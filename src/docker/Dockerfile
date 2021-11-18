# syntax = docker/dockerfile:1.0-experimental

FROM python:3.9
COPY requirements.txt ${FUNCTION_DIR}

RUN --mount=type=secret,id=pipconfig,dst=/etc/pip.conf \
    pip install -r requirements.txt

ENV TRANSFORM_INSTANCE_CONTEXT default
ENV TRANSFORM_NID default

COPY entrypoint.py ${FUNCTION_DIR}
ENTRYPOINT [ "python", "entrypoint.py" ]