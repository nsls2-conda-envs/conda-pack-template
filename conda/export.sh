#!/bin/bash

set -e

echo "Environment name: ${env_name}"
echo "Channels: ${channels}"

conda activate ${env_name}
#while read requirement;do conda install --yes ${channels} --override-channels ${requirement};done < /requirements.txt
conda env export -n ${env_name} -f ${env_name}.yml ${channels} --override-channels
conda-pack -o ${env_name}.tar.gz
openssl sha256 ${env_name}.tar.gz > ${env_name}-sha256sum.txt
chmod -v 664 ${env_name}[.-]*
conda deactivate
