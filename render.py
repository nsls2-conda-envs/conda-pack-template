import os

from jinja2 import Template

params = {
    # "docker_image": "nsls2/debian-with-miniconda:v0.1.2",
    "docker_image": "quay.io/condaforge/linux-anvil-comp7:latest",
    "env_name": "astra-toolbox",
    "python_version": "3.8",
    "pkg_name": "",
    "pkg_version": "",
    "extra_packages": "astra-toolbox tomopy",
    "channels": "-c astra-toolbox/label/dev -c conda-forge",
}

script_location = os.path.abspath(os.path.dirname(__file__))
print(f"Script location: {script_location}")
template_file = os.path.join(script_location, "gen-conda-packed-env.sh.j2")
name = os.path.splitext(os.path.splitext(os.path.basename(template_file))[0])
script_name = f"{name[0]}-{params['env_name']}{name[1]}"
params["script_name"] = script_name

with open(template_file) as f:
    template = Template(f.read())

text = template.render(**params)
print(text)

with open(script_name, "w") as f:
    f.write(text)
