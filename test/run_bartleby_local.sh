#!/usr/bin/env bash

if [ -n "$1" ]; then
  echo "Generating docs for $1"
else
  echo "Enter a repo name to generate docs for"
  exit
fi

if [ -n "$2" ]; then
  shell_in="${@/$1/""}"
  shell_in=${shell_in/ /}
  export SPHINX_CMD="{\"shell\": \"$shell_in\"}"
else
  export SPHINX_CMD="{\"shell\": \"default\"}"
fi

pushd "$HMD_REPO_HOME/hmd-tf-bartleby"

cp -r src/docker/doctools test/src/docker
cp -r src/python/hmd_tf_bartleby test/src/docker/python

popd

hmd --repo-name hmd-tf-bartleby --repo-version test docker build

docker run -it --rm \
-v "$HMD_REPO_HOME/$1/docs:/hmd_transform/input" \
-v "$HMD_REPO_HOME/$1/target/bartleby:/hmd_transform/output" \
-v "$HMD_HOME/bartleby/log:/tmp" \
-e "TRANSFORM_INSTANCE_CONTEXT=$SPHINX_CMD" \
-e "HMD_DOC_REPO_NAME=$1" \
-e "HMD_DOC_REPO_VERSION=0.1" \
ghcr.io/hmdlabs/hmd-tf-bartleby:test