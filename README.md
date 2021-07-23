# Conda-pack template & rendering script to generate conda-pack'd envs.

## Example

To render the configuration, run the following command:

### Command:

```bash
$ python render.py -c configs/n2sn.yml
```

### Output:

```bash
Script location: /Users/mrakitin/tmp/docker-build/conda-pack-template
#!/bin/bash

# To be run as:
# $ docker run -it --rm -v $PWD:/build quay.io/condaforge/linux-anvil-comp7:latest bash /build/gen-conda-packed-env-n2sn.sh

set -e

umask 0002

. /opt/conda/etc/profile.d/conda.sh

conda install conda -y

env_name="n2sn"
python_version="=3.9"
pkg="n2snusertools=0.3.6"
extra_packages=""
channels="-c nsls2forge -c defaults"

time conda create \
    -n ${env_name} \
    ${channels} --override-channels -y \
    python${python_version} conda-pack \
    ${pkg} \
    ${extra_packages}

conda activate ${env_name}

time conda env export \
    -n ${env_name} \
    -f /build/${env_name}.yml \
    ${channels} --override-channels

# Assuming the "build" dir is mounted via the "docker run -v ..."
time conda-pack -o /build/${env_name}.tar.gz

time openssl sha256 /build/${env_name}.tar.gz > /build/${env_name}-sha256sum.txt
chmod -v 664 /build/${env_name}[.-]*

conda deactivate
```

That should result in a file named `gen-conda-packed-env-n2sn.sh` in the current directory.
For other configurations, a differently named file will be created.
