import os
from pathlib import Path
import yaml
from pyzenodo3.upload import upload
import argparse

def upload_to_zenodo(file_name_to_upload, base_url="https://sandbox.zenodo.org/api/"):
    upload(
        datafn=Path(file_name_to_upload),
        token=os.getenv("ZENODO_ACCESS_TOKEN", ""),
        metafn="",
    )

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description=(
            "Upload files to Zenodo."
        )
    )
    parser.add_argument(
        "-f", "--file", dest="file_name_to_upload", help="the input config file"
    )
    args = parser.parse_args()
    upload_to_zenodo(args.file_name_to_upload)
    print("Upload Done!")
