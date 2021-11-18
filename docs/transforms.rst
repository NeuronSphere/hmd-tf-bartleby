.. transforms

Anatomy of an HMD Transform
===============================

An HMD Transform can take many forms, but it has at a minimum a mini context and basic project structure that supports
docker and python.

Context:
+++++++++
#. TRANSFORM_INSTANCE_CONTEXT: the configuration for a Transform instance

    - Type: json
    - Default: standard input defined in the respective transform engine
    - Custom: input supplied as an argument in the CLI

#. NID_CONTEXT: the set of entity identifiers from the global graph database that indicate a Transform is needed. These
   include the Transform instance identifier that is used to upsert relationship(s) between the
   output and the instance

    - Type: json
    - Default: nids corresponding to entities in scope of the transform service (based on state)
    - Custom: input supplied as an argument in the CLI

    *For example, a CAN Transform nid context includes a librarian manifest nid and transform nid*

#. I/O directories: file system which can be shared between multiple docker
   images and ultimately serve to transport the transformed content through the Transform workflow

    - Type: directory
    - Default: ``/hmd_transform/input``, ``/hmd_transform/output``

Project Structure:
+++++++++++++++++++
#. Docker:
    - *Dockerfile*: defines variables for the context and copies in the entrypoint script

    .. code-block:: dockerfile

        FROM python:3.9
        COPY requirements.txt ${FUNCTION_DIR}

        RUN --mount=type=secret,id=pipconfig,dst=/etc/pip.conf \
            pip install -r requirements.txt

        ENV TRANSFORM_INSTANCE_CONTEXT default
        ENV TRANSFORM_NID default

        COPY entrypoint.py ${FUNCTION_DIR}
        ENTRYPOINT [ "python", "entrypoint.py" ]


    - *entrypoint.py*: the script used to import the python package

    .. code-block:: python

        from <repo_name>.<repo_name> import entry_point

        if __name__ == "__main__":
            entry_point()



#. Python:
    - *<module_name>.py*: the code to implement the transformation

    A basic structure is provided to set up logging, context variables and enable the entrypoint script to successfully
    import the python package. Additionally, a basic transform is defined under ``do_transform()`` in order to
    illustrate how the context is used and how the code is tested.

    .. code-block:: python

        import logging
        import sys
        import os
        from pathlib import Path

        logging.basicConfig(
            stream=sys.stdout,
            format="%(levelname)s %(asctime)s - %(message)s",
            level=logging.ERROR,
        )

        logger = logging.getLogger(__name__)
        logger.setLevel(logging.DEBUG)


        def entry_point():

            # initialize variables for transform I/O
            input_content_path = Path("/hmd_transform/input")
            output_content_path = Path("/hmd_transform/output")

            # assign context to variables
            transform_instance_context = os.environ.get("TRANSFORM_INSTANCE_CONTEXT")
            transform_nid = os.environ.get("TRANSFORM_NID")

#. Meta-data:
    - *manifest.json*: defined with a standard structure to support python and docker commands

#. Test:
    - Test_suite:
        - *01__transform_build.robot*: robot test template with a single test case that executes the hmd docker build
          command. Typically, the script used to run the suite will include steps to copy the docker and python source
          files into the test folder appropriately so that the hmd docker build command can locate the Dockerfile and
          execute the build successfully. However, in order to produce a usable test the files have been renamed with a
          legal python module name and included directly in the test folder.
        - *02__transform_run.robot*: robot test template with a templated test case that runs the transform container in
          a docker compose environment with expected mounts and environment variables. The compose file also
          demonstrates how to read secrets into the container securely and the output of the transform is verified as
          part of the test case for each given set of inputs.

        .. note::
            Proper sequencing of the files within the test suite is dependent upon the naming convention used.
            Specifically, the file names must start with ``01__``, ``02__``, ``03__``, etc. in order for robot to
            interpret the sequence correctly.

    - Running the robot tests:

        Use the code below to execute the test suite.

        .. code-block:: bash

            robot --pythonpath ./test_suite \
            --settag hmd_repo_name:$HMD_REPO_NAME \
            --settag hmd_repo_version:$HMD_REPO_VERSION \
            --settag hmd_did:$HMD_DID \
            --include Transform* \
            test_suite

        The ``--include`` parameter can be modified to ``--include Transform_run`` for efficiency if the image has
        already been built and does not need to be executed again. The ``--settag`` parameters will force tags onto each
        of the executed test cases within the suite to ensure all cases are properly labeled with standard HMD variables.