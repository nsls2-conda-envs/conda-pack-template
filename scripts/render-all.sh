#!/bin/bash

set -vxeuo pipefail

oneshot=${1:-}

for f in $(ls -1 configs/*.yml); do
    echo $f
    if [ -z "${oneshot}" ]; then
        dockerfile=$(python3 render.py -c ${f} -f Dockerfile.j2)
        runner_script=$(python3 render.py -c ${f} -f runner.sh.j2)
    elif [ "${oneshot}" == "oneshot" ]; then
        res=($(python3 render.py -c ${f} -f Dockerfile.j2 -f runner.sh.j2))
        dockerfile=${res[0]}
        runner_script=${res[1]}
    else
        echo "Unknown option for 'oneshot': ${oneshot}. It should either be empty or be 'oneshot'"
        exit 1
    fi
    echo $dockerfile
    cat ${dockerfile}

    echo $runner_script
    cat ${runner_script}
done

