.. Packaging Scientific Python documentation master file, created by
   sphinx-quickstart on Thu Jun 28 12:35:56 2018.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

conda-pack-template
===================

The ``conda-pack-template`` is a light framework for generation and packaging
of custom conda environments.

The conda environments are specified by a configuration YAML file, e.g.
``config-py39.yml`` from
https://github.com/nsls2-conda-envs/testenv/tree/main/configs:

.. code::

    docker_image: "nsls2/linux-anvil-cos7-x86_64:latest"
    env_name: "py39"
    conda_env_file: "env-py39.yml"
    conda_binary: "mamba"
    python_version: "3.9"
    pkg_name: ""
    pkg_version: ""
    extra_packages: "mamba"
    channels: "-c conda-forge"

where the required parameters are:

- ``docker_image`` is the image to use for building in a containerized
  environment
- ``env_name`` is the name of the environment to be created
- ``python_version`` is the Python version to use (not used when the
  environment file is used)
- ``channels`` lists the conda channels

and the optional parameters are:

- ``conda_env_file`` is  the `conda environment
  file
  <https://conda.io/projects/conda/en/latest/user-guide/tasks/manage-environments.html#creating-an-environment-file-manually>`_
- ``conda_binary`` is the conda binary --- ``conda`` (default) or ``mamba``
  (for faster execution)
- ``pkg_name`` is the conda package to install (can be an empty string)
- ``pkg_version`` is the version of the ``pkg_name``
- ``extra_packages`` lists the extra conda packages to install along with
  ``pkg_name``
- ``extra_cmd_before_install`` (not listed in the above example) is used to
  specify the command to run in Docker before conda environment installation
- ``extra_cmd_after_install`` (not listed in the above example) is used to
  specify the command to run in Docker after conda environment installation

.. note::

   The repository is not structured to be a pip-installable package (yet).
   However, its code will be used to process individual conda environment
   configurations managed via separate repositories (one repo per environment).

.. toctree::
   :maxdepth: 2

   installation
   usage

.. toctree::
   :hidden:
   :caption: Links

   conda-pack-template GitHub repo <https://github.com/nsls2-conda-envs/conda-pack-template>
