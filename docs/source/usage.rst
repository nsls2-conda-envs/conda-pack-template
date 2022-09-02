=====
Usage
=====

The following steps will generate the ``Dockerfile`` and the ``runner-*.sh``
files (from the Jinja2 templates using the parameters from the YAML
configuration file). These files will be used afterwards to run the build of
the environment.

Create a Dockerfile
-------------------

In order to build the conda environment for a specific platform (e.g., Linux),
we create a Docker image matching the target platform. Even if the environment
is built on a specific Linux version, such as CentOS7, it can still be used for
other Linux flavors (e.g., Debian, RedHat, etc.) as long as the version of
**glibc** on the target platform is higher than the one in the build system's
OS.

.. note::

   Please refer to https://conda.github.io/conda-pack for the limitations.
   E.g., the OS where the environment was built must match the OS of the
   target. This means that environments built on Windows can't be relocated to
   Linux.

At top level of the repository, generate the ``Dockerfile`` with this command:

.. code-block:: bash

   python3 render.py -c configs/<env-name>.yml -f Dockerfile.j2

The resulting ``Dockerfile`` will contain the instructions on how to build the
corresponding Docker image with the conda environment inside. The conda
environment is specified either via the environment file, or with the list of
packages and extra-packages.


Create a runner script
----------------------

The runner script is used to (i) build the Docker image based on the
``Dockerfile`` from the previous step, (ii) run a Docker container based on
that image with a mounted host directory, and (iii) export the artifacts to the
``artifacts/`` directory on the host system.

To generate the ``runner-*.sh`` file, run this command:

.. code-block:: bash

   python3 render.py -c configs/<env-name>.yml -f runner.sh.j2


Run the build
-------------

Run the resulting ``runner-*.sh`` file:

.. code-block:: bash

   bash ./runner-<env-name>.sh

After running this script, the following files will be produced in the
``artifacts/`` directory:

- ``<env-name>.tar.gz`` is the tarball with the conda environment packaged with
  conda-pack;
- ``<env-name>-md5sum.txt`` and ``<env-name>-sha256sum.txt`` are the files
  containing MD5 and SHA256 checksums respectively, which can be used to
  validate the integrity of the tarball file in various places (e.g., Zenodo
  uses MD5 checksums, while NSLS-II Ansible deployment roles use SHA256
  checksums);
- ``<env-name>.yml`` is the file produced by the ``conda env export`` command,
  which lists all the packages and their versions in the conda environment.
