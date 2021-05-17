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

    script_location = os.path.abspath(os.path.dirname(__file__))
    print(f"Script location: {script_location}")
    template_file = os.path.join(script_location, "gen-conda-packed-env.sh.j2")
    # Get the base name, i.e. 'gen-conda-packed-env.sh':
    name = os.path.splitext(os.path.basename(template_file))[0]
    # Split the base name into ('gen-conda-packed-env', '.sh'):
    name = os.path.splitext(name)
    script_name = f"{name[0]}-{params['env_name']}{name[1]}"
    params["script_name"] = script_name

    with open(template_file) as f:
        template = Template(f.read())

    text = template.render(**params)
    print(text)

    with open(script_name, "w") as f:
        f.write(text)
