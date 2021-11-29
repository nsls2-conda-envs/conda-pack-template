#!/bin/bash

set -vxeuo pipefail

ls -laF ${build_dir}

env | sort -u

echo "Environment name: ${env_name}"
echo "Channels        : ${channels}"
echo "Build dir       : ${build_dir}"

source /opt/conda/etc/profile.d/conda.sh

conda activate ${env_name}
conda env export -n ${env_name} -f ${build_dir}/${env_name}.yml ${channels} --override-channels
conda-pack -o ${build_dir}/${env_name}.tar.gz
openssl sha256 ${build_dir}/${env_name}.tar.gz > ${build_dir}/${env_name}-sha256sum.txt
openssl md5 ${build_dir}/${env_name}.tar.gz > ${build_dir}/${env_name}-md5sum.txt
chmod -v 664 ${build_dir}/${env_name}[.-]*
# conda deactivate
