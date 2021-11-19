# syntax = docker/dockerfile:1.0-experimental

FROM sphinxdoc/sphinx-latexpdf
COPY doctools /hmd_transform/doctools
COPY requirements.txt .

COPY python .

RUN --mount=type=secret,id=pipconfig,dst=/etc/pip.conf \
    pip install -r requirements.txt

RUN python setup.py sdist bdist_wheel
RUN pip install -U --no-index --no-deps --force-reinstall --find-links=./dist hmd-tf-bartleby==0.0.1

ENV TRANSFORM_INSTANCE_CONTEXT default
ENV TRANSFORM_NID default

WORKDIR /app
COPY entrypoint.py .
ENTRYPOINT [ "python", "entrypoint.py" ]