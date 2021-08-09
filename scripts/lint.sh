#!/bin/bash

set -vxeuo pipefail

script_dir=$(dirname ${0})

# isort
${script_dir}/isort.sh

# black
${script_dir}/black.sh

# flake8
${script_dir}/flake8.sh
