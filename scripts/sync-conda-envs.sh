#!/bin/bash

staged_envs_path="/conda-envs-staging"
conda_envs_path="/nsls2/repos/conda/environments"

owner="nsls2data"
group="nsls2software"

allowed_extensions=(".tar.gz" ".yml" "md5sum.txt" "sha256sum.txt")

for ext in ${allowed_extensions[@]}; do
    new_files_exist=$(ls -1 ${staged_envs_path}/*${ext} 2>/dev/null)
    if [ ! -z "${new_files_exist}" ]; then
        echo -e "Files with extension '${ext}' exist:\n\n${new_files_exist}\n"
        mv -v ${staged_envs_path}/*${ext} ${conda_envs_path}/
    else
        echo -e "NO files with extension '${ext}' exist:\n\n${new_files_exist}\n"
    fi
    unset new_files_exist
done

chown -v ${owner}:${group} ${conda_envs_path}/*
chmod -v 664 ${conda_envs_path}/*

exit 0
