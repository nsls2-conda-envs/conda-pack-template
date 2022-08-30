============
Installation
============

The system requires Docker or Podman to run successfully. Please follow the
corresponding instructions at:

- https://docs.docker.com/get-docker/
- https://podman.io/getting-started/

Then, at the command line run the following command to install dependencies::

    $ python3 -m pip install -r requirements.txt

Current list of dependencies:

.. include:: ../../requirements.txt
   :literal:

The ``jinja2``, and ``pyyaml`` packages are required dependencies, the rest is
optional for convenience.
