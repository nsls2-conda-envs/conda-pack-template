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
        params.setdefault('docker_upload', "dockerhub;ghcr;quay")
        params.setdefault('zenodo_upload', "yes")
        os.environ.update(params)

    script_location = os.path.abspath(os.path.dirname(__file__))
    print(f"Script location: {script_location}")

    # RENDER runner.sh
    template_file = os.path.join(script_location, "runner.sh.j2")
    # Get the base name, i.e. 'gen-conda-packed-env.sh':
    name = os.path.splitext(os.path.basename(template_file))[0]
    # Split the base name into ('gen-conda-packed-env', '.sh'):
    name = os.path.splitext(name)
    script_name = f"{name[0]}-{params['env_name']}{name[1]}"
    params["script_name"] = script_name

    with open(template_file) as f:
        template = Template(f.read())

    text = template.render(os=os, config_file=args.config_file, **params)
