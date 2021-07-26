import os
from pathlib import Path
import yaml
from pyzenodo3.upload import upload

def upload_to_zenodo(config_file="n2sn.yml"):
    with open(config_file, "r") as fp:
        yaml_file = yaml.load(fp, Loader=yaml.BaseLoader)
        upload(
            datafn=Path(yaml_file.get("zenodo_upload_file_path")),
            token=os.getenv("ZENODO_ACCESS_TOKEN", ""),
            base_url="https://sandbox.zenodo.org/api/",
            metafn=Path(""),
        )

if __name__ == "__main__":
    upload_to_zenodo()
    print("Upload Done!")
