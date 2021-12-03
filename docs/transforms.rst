.. transforms

Bartleby Transform
===============================

The bartleby transform engine is HMD's document rendering and packaging tool. It takes as its input a repository name along
with the desired document format and produces the formatted documents as its output. The document generation features
are simply extensions of the Sphinx documentation generator tools, while the automation features are based upon HMD's
repository standards.


Context:
+++++++++
#. TRANSFORM_INSTANCE_CONTEXT: the output document format for a ``transform_instance``

    - Type: json
    - Default: Blank (displays the Sphinx help menu for the 'make' command)
    - Custom: input supplied as an argument in the CLI

    *Configured options*: html, latexpdf

#. NID_CONTEXT: the entity identifier from the global graph database for the ``repo_instance`` where a bartleby
   transform is needed. This also includes the ``transform_instance`` identifier that is used to upsert relationship(s)
   between the output entities and the instance

    - Type: json
    - Default: nids corresponding to ``repo_instance`` entities with "deploy_next" state in the global graph database;
      bartleby transform instance nids for the ``transform_instance`` entities created by the transform manager
    - Custom: input supplied as an argument in the CLI; used as the ``repo_instance`` entity for ad-hoc cases where
      generated documents are needed

    *Entities automatically picked up by the transform manager graph query*:

    - Entity name: ``hmd_lang_deployment.repo_instance``
    - Entity state: DEPLOY_NEXT


#. I/O directories: file system which can be shared between multiple docker
   images and ultimately serve to transport the transformed content through the Transform workflow

    - Type: directory
    - Default: ``/hmd_transform/input``, ``/hmd_transform/output``

Project Structure:
+++++++++++++++++++
#. Docker:
    - *Dockerfile*: defines variables for the context and copies in the entrypoint script; the bartleby image is built
      from the sphinx docker image and also includes a java runtime environment and external java packages needed for
      generating plantuml diagrams.

    - *entrypoint.py*: the script used to import the python package

    .. code-block:: python

        from <repo_name>.<repo_name> import entry_point

        if __name__ == "__main__":
            entry_point()


    - *doctools*: directory for the sphinx documentation generator tools as configured for the bartleby transform; the
      directory contains the following:

        - *source* directory: configuration file, templates and other static resources used for generating documents.

        .. note::
            A separate ``conf.py`` may be provided as part of the transform input by including the file in the docs
            folder of a given repository (alongside the ``index.rst`` file)

        - *make.bat*: default sphinx command file

        - *Makefile*: default sphinx makefile

#. Python:
    - *hmd_tf_bartleby.py*: the code to implement the transformation


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

    - *run_test.sh*:

        Use the code below to execute the test suite locally.

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

    - *run_bartleby_local.sh*: script used to build and run the bartleby transform locally (to be replaced by bartleby
      CLI); run the script as follows:

        .. code-block:: bash

            bash run_bartleby_local.sh <repo_name> <target_format>

        .. note::
            See *configured options* under TRANSFORM_INSTANCE_CONTEXT for ``target_format`` options



A CLI
==============================
Some of this content should be moved to a more standard location for 'cli-ing a transform'.

The idea of a CLI for bartleby or any other transform is similar - the executable communicates with the docker
daemon via a library to launch and manage a transform with a particular set of volume mappings and configurations.

This "CLI" would reasonably be called a "wrapper" or perhaps an "adaptor" with regard to the actual transform image.

One of the things that makes a CLI useful is passing parameters to control a program's behavior. A Transform CLI wrapper
maps user entered CLI parameters onto the mechanisms the transform image requires in order to work.  In the case of
Bartleby (and many others), the parameters to the CLI will be "passed through" to the transform as a single blob via the
transform context and the 'shell' key.

The assumption is that the CLI is run 'above or within' a standard repository.  If run from <repo_root>/ it operates on
the current repository (mounting it to both input and output of the transform).  If run from other locations the path to
the repo root is the first CLI parameter (or we may have to use -r as below?)

Thus running 'hmd bartleby pdf' within $HMD_REPO_HOME/hmd-lib-demo, you'll get the pdf outputs in
$HMD_REPO_HOME/hmd-lib-demo/target/bartleby

From $HMD_REPO_HOME, one could run 'hmd bartleby -r hmd-lib-demo pdf'.

Note the cli wrapper should do a thorough job of disposing of the temporal container and any associated resources.