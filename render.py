import argparse
import os

import yaml
from jinja2 import Template


def read_params(config_file):
    if not os.path.isfile(config_file):
        raise RuntimeError(f"The config file '{config_file}' is not found.")

    with open(config_file) as f:
        params = yaml.load(f, Loader=yaml.SafeLoader)

    params.setdefault("docker_upload", ["dockerhub", "ghcr", "quay"])
    params.setdefault("conda_binary", "conda")
    params.setdefault("conda_env_file", None)

    zenodo_metadata_present = params.pop(
        "zenodo_metadata", None
    )  # removing the parameters that are not needed for rendering
    if zenodo_metadata_present:
        params.setdefault("zenodo_upload", "no")

    return params


def validate_templates_dir(templates_dir):
    script_location = os.path.abspath(os.path.dirname(__file__))
    templates_dir = os.path.join(script_location, templates_dir)
    if not os.path.isdir(templates_dir):
        raise FileNotFoundError(
            f"The templates directory '{templates_dir}' does not exist."
        )
    return templates_dir


def validate_template_file(template_file, templates_dir):
    script_location = os.path.abspath(os.path.dirname(__file__))
    template_file = os.path.join(script_location, templates_dir, template_file)
    if not os.path.isfile(template_file):
        raise FileNotFoundError(
            f"The template file '{template_file}' does not exist."
        )
    return template_file


def _render_file(template_file, output_file, debug=False, **params):
    with open(template_file) as f:
        template = Template(f.read())

    text = template.render(params=params, **params)
    if debug:
        print(text)

    with open(output_file, "w") as f:
        f.write(text)


def render_runner(template_file, **params):
    # Get the base name, i.e. 'runner.sh':
    name = os.path.splitext(os.path.basename(template_file))[0]
    # Split the base name into ('runner', '.sh'):
    name = os.path.splitext(name)

    output_file = f"{name[0]}-{params['env_name']}{name[1]}"
    params["script_name"] = output_file

    _render_file(
        template_file=template_file, output_file=output_file, **params
    )

    return params, output_file


def render_dockerfile(template_file, **params):
    # Get the base name, i.e. 'Dockerfile':
    name = os.path.splitext(os.path.basename(template_file))[0]

    output_file = f"{name}"
    params["script_name"] = output_file

    _render_file(
        template_file=template_file, output_file=output_file, **params
    )

    return params, output_file


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description=(
            "Render a generation script based on the specified config"
            "file to produce a conda-pack'd environment."
        )
    )
    parser.add_argument(
        "-c",
        "--config-file",
        dest="config_file",
        required=True,
        help="the input config file",
    )
    parser.add_argument(
        "-d",
        "--templates-dir",
        dest="templates_dir",
        default="templates",
        help="the templates directory",
    )
    parser.add_argument(
        "-f",
        "--template-file",
        dest="template_file",
        required=True,
        help="the template to render",
    )
    args = parser.parse_args()

    params = read_params(args.config_file)
    templates_dir = validate_templates_dir(args.templates_dir)
    template_file = validate_template_file(args.template_file, templates_dir)

    if template_file.endswith("runner.sh.j2"):
        params, output_file = render_runner(
            template_file=template_file, **params
        )
    elif template_file.endswith("Dockerfile.j2"):
        params, output_file = render_dockerfile(
            template_file=template_file, **params
        )
    else:
        parser.exit(f"Unknown template file: {template_file}")

    print(output_file)  # used by CI to get the file name
