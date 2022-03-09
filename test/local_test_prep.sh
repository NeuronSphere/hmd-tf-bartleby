#!/usr/bin/env bash

pushd "$HMD_REPO_HOME/hmd-tf-bartleby"

cp -r src/docker/doctools test/src/docker
cp -r src/docker/__init__.py test/src/docker
cp -r src/docker/entry_puml.py test/src/docker
cp -r src/python/hmd_tf_bartleby test/src/docker/python

popd

hmd --repo-name hmd-tf-bartleby --repo-version test docker build

