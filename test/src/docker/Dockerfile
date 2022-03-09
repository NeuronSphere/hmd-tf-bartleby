# syntax = docker/dockerfile:1.0-experimental

FROM sphinxdoc/sphinx-latexpdf
COPY doctools /hmd_transform/doctools
COPY requirements.txt .

COPY python .

RUN apt-get update
RUN apt install -y curl
RUN curl -L "https://sourceforge.net/projects/plantuml/files/1.2021.14/plantuml.1.2021.14.jar/download" -o /usr/local/bin/plantuml.jar

RUN apt install -y default-jre

RUN apt install -y libpq-dev python3-dev postgresql gcc

RUN --mount=type=secret,id=pipconfig,dst=/etc/pip.conf \
    pip install -r requirements.txt

RUN python setup.py sdist bdist_wheel
RUN pip install -U --no-index --no-deps --force-reinstall --find-links=./dist hmd-tf-bartleby==0.0.1

#COPY __init__.py /usr/local/lib/python3.10/site-packages/sphinx/ext/autodoc/

ENV TRANSFORM_INSTANCE_CONTEXT default
ENV NID_CONTEXT default

WORKDIR /app
COPY entrypoint.py .
COPY entry_puml.py .

CMD [ "python", "entrypoint.py" ]