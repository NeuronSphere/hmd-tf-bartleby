# syntax = docker/dockerfile:1.0-experimental

FROM python:3.9
COPY requirements.txt ${FUNCTION_DIR}

COPY python .

RUN python setup.py sdist bdist_wheel
RUN pip install -U --no-index --no-deps --force-reinstall --find-links=./dist module_name==0.0.1

ENV TRANSFORM_INSTANCE_CONTEXT default
ENV TRANSFORM_NID default

COPY entrypoint.py ${FUNCTION_DIR}
ENTRYPOINT [ "python", "entrypoint.py" ]