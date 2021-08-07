import argparse
import json
import os

import requests
import yaml


def upload_to_zenodo(
    file_name_to_upload,
    config_file,
    zenodo_server="https://sandbox.zenodo.org/api/deposit/depositions",
):
    filename = os.path.abspath(file_name_to_upload)
    if not os.path.isfile(filename):
        raise FileNotFoundError(
            f"The file, specified for uploading does not exist: {filename}"
        )

    config_name = os.path.abspath(config_file)
    if not os.path.isfile(config_name):
        raise FileNotFoundError(
            f"The file with metadata, specified for uploading does not exist: "
            f"{config_name}"
        )

    headers = {"Content-Type": "application/json"}
    params = {"access_token": os.getenv("ZENODO_ACCESS_TOKEN", "")}
    r = requests.post(
        zenodo_server,
        params=params,
        json={},
        headers=headers,
    )
    if r.status_code != 201:
        raise RuntimeError(
            f"The status code for the request is {r.status_code}.\n"
            f"Message: {r.text}"
        )

    return_json = r.json()
    deposition_id = return_json["id"]
    bucket_url = return_json["links"]["bucket"]

    filebase = os.path.basename(file_name_to_upload)

    file_url = return_json["links"]["html"].replace("deposit", "record")

    print(f"Uploading {filename} to Zenodo. This may take some time...")
    with open(filename, "rb") as fp:
        r = requests.put(f"{bucket_url}/{filebase}", data=fp, params=params)
        if r.status_code != 200:
            raise RuntimeError(
                f"The status code for the request is {r.status_code}.\n"
                f"Message: {r.text}"
            )
        print(f"\nFile Uploaded successfully!\nFile link: {file_url}")

    print(f"Uploading metadata for {filename} ...")
    with open(config_file) as fp:

        data = yaml.safe_load(fp)

        r = requests.put(
            f"{zenodo_server}/{deposition_id}",
            params=params,
            data=json.dumps(data["zenodo_metadata"]),
            headers=headers,
        )
        if r.status_code != 200:
            raise RuntimeError(
                f"The status code for the request is {r.status_code}.\n"
                f"Message: {r.text}"
            )

    print(f"Publishing {filebase}...")
    r = requests.post(
        f"{zenodo_server}/{deposition_id}/actions/publish", params=params
    )
    if r.status_code != 202:
        raise RuntimeError(
            f"The status code for the request is {r.status_code}.\n"
            f"Message: {r.text}"
        )


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=("Upload files to Zenodo."))
    parser.add_argument(
        "-f",
        "--file",
        dest="file_name_to_upload",
        help="path to the file to be uploaded",
    )
    parser.add_argument(
        "-c",
        "--config-file",
        dest="config_file",
        help="config file with metadata information",
    )

    args = parser.parse_args()
    upload_to_zenodo(args.file_name_to_upload, args.config_file)
