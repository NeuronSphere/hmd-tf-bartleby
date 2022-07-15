#!/usr/bin/env bash

winpty docker run --rm -it \
-v "${HMD_HOME}/bartleby/tests://hmd_transform/output" \
-v "${HMD_REPO_HOME}/hmd-lib-librarian-client/docs://hmd_transform/input" \
-v "${HMD_REPO_HOME}/hmd-tf-bartleby/test/env/Lib/site-packages:/usr/local/lib/python3.10/site-packages" \
-v "${HMD_REPO_HOME}/hmd-tf-bartleby/src/docker/doctools://hmd_transform/doctools" \
-v "${HMD_HOME}/bartleby/pip://run/secrets/pip_url" \
-e "TRANSFORM_INSTANCE_CONTEXT={\"shell\": \"html\"}" \
-e "AUTODOC=True" \
-e "HMD_DOC_REPO_NAME=hmd-lib-librarian-client" \
-e "HMD_DOC_REPO_VERSION=0.1" \
-e "PIP_CONF=//run/secrets/pip_url/pip.conf" \
ghcr.io/hmdlabs/hmd-tf-bartleby:0.1
