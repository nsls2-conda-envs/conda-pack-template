import os

from jinja2 import Template

params = {
    # "docker_image": "nsls2/debian-with-miniconda:v0.1.2",
    "docker_image": "quay.io/condaforge/linux-anvil-comp7:latest",
    "env_name": "bmm-analysis",
    "python_version": "3.9",
    "pkg_name": "",
    "pkg_version": "",
    "extra_packages": "numpy scipy hdf5 matplotlib pyqt pyyaml pyside2",
    "channels": "-c conda-forge",
}

template_file = "gen-conda-packed-env.sh.j2"
name = os.path.splitext(os.path.splitext(template_file)[0])
script_name = f"{name[0]}-{params['env_name']}{name[1]}"
params["script_name"] = script_name

with open(template_file) as f:
    template = Template(f.read())

text = template.render(**params)
print(text)

with open(script_name, "w") as f:
    f.write(text)
