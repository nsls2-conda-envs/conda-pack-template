==========================
Frequently Asked Questions
==========================

Synchronize environment files
-----------------------------

The ``nsls2-collection`` and ``nsls2-collection-tiled`` repositories are very
similar in terms of the packages and should be updated in tandem. The
difference is only in the ``databroker`` package which should have versions
``>=1.2.5,<2.0.0a`` in the ``nsls2-collection`` repository, and ``>=2.0.0b`` in
the ``nsls2-collection-tiled`` repository. The former is also coming with the
``databroker-pack`` and ``intake`` packages while the latter contains the
``tiled`` package (hence the repository name).

When creating a new version of the conda environments, e.g. ``2023-3.0-py310``,
one would create a new feature branch from ``main``, then update the
``configs/config-py310.yml`` file with the corresponding version as well as the
``envs/env-py310.yml`` file with the new pins of the existing packages and/or
new packages. Once this was done for one repository (preferably via one
commit), e.g. for ``nsls2-collection``, create a patch file as follows:

.. code-block:: bash

   git format-patch -1

This will produce a file such as ``0001-2023-3.0-env.patch``. Then, navigate to
another repository (``nsls2-collection-tiled``) and apply this patch as
follows:

.. code-block:: bash

   patch -p1 < ../nsls2-collection/0001-2023-3.0-env.patch

This may result in an incomplete application of the patch, as there may be
conflicting changes applied to both repositories in the same files/places
(e.g., the environment names will be ``2023-3.0-py310`` vs.
``2023-3.0-py310-tiled`` in both config and environment files). Nevertheless,
the rest of the updates will be applied correctly. You may consider separating
commits for the environment version update and the packages version update to
reduce the number of conflicts.

It is recommended always to check the difference between the repositories.
Change to the common directory where both repositories are cloned and then run
the command such as:

.. code-block:: bash

   diff nsls2-collection/envs/env-py310.yml nsls2-collection-tiled/envs/env-py310.yml
