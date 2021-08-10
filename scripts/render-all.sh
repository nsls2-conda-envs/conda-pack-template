#!/bin/bash

set -vxeuo pipefail

for f in $(ls -1 configs/*.yml); do
    echo $f
    dockerfile=$(python3 render.py -c ${f} -f Dockerfile.j2)
    runner_script=$(python3 render.py -c ${f} -f runner.sh.j2)
    echo $dockerfile
    cat ${dockerfile}

    echo $runner_script
    cat ${runner_script}
done

