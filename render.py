import argparse
import os

import yaml
from jinja2 import Template

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description=(
            "Render a generation script based on the specified config"
            "file to produce a conda-pack'd environment."
        )
    )
    parser.add_argument(
        "-c", "--config-file", dest="config_file", help="the input config file"
    )
    args = parser.parse_args()

    config_file = os.path.abspath(args.config_file)

    if not os.path.isfile(config_file):
        raise RuntimeError(f"The config file '{config_file}' is not found.")

    with open(config_file) as f:
        params = yaml.load(f, Loader=yaml.SafeLoader)
    params.setdefault('docker_upload', ['dockerhub', 'ghcr', 'quay'])
    zenodo_metadata_present = params.pop(
        'zenodo_metadata', None
    )  # removing the parameters that are not needed for rendering
    if zenodo_metadata_present:
        params.setdefault('zenodo_upload', 'yes')

    script_location = os.path.abspath(os.path.dirname(__file__))
    templates_dir = os.path.join(script_location, 'templates')
    if not os.path.isdir(templates_dir):
        raise FileNotFoundError(f"The directory '{templates_dir}' does not exist.")

    print(f"Script location: {script_location}")

    # RENDER runner.sh
    template_file = os.path.join(templates_dir, "runner.sh.j2")
    # Get the base name, i.e. 'runner.sh':
    name = os.path.splitext(os.path.basename(template_file))[0]
    # Split the base name into ('runner', '.sh'):
    name = os.path.splitext(name)
    script_name = f"{name[0]}-{params['env_name']}{name[1]}"
    params["script_name"] = script_name

    with open(template_file) as f:
        template = Template(f.read())

    text = template.render(params=params, **params)
    print(text)

    with open(script_name, "w") as f:
        f.write(text)

    # RENDER Dockerfile
    template_file = os.path.join(templates_dir, "Dockerfile.j2")

    name = os.path.splitext(os.path.basename(template_file))[0]

    script_name = f"{name}"
    params["script_name"] = script_name

    with open(template_file) as f:
        template = Template(f.read())

    text = template.render(**params)
    print(text)

    with open(script_name, "w") as f:
        f.write(text)
