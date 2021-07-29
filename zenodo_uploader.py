import os

import argparse
import requests
import yaml
import json

def upload_to_zenodo(
    file_name_to_upload,
    zenodo_server="https://sandbox.zenodo.org/api/deposit/depositions",
):
    headers = {"Content-Type": "application/json"}
    params = {"access_token": os.getenv("ZENODO_ACCESS_TOKEN", "")}
    r = requests.post(
        zenodo_server,
        params=params,
        json={},
        headers=headers,
    )
    if r.status_code != 201:
        raise RuntimeError(f"The status code for the request is {r.status_code}.\nMessage: {r.text}")

    return_json = r.json()
    deposition_id = return_json["id"]
    bucket_url = return_json["links"]["bucket"]

    filename = os.path.abspath(file_name_to_upload)
    filebase = os.path.basename(file_name_to_upload)

    if not os.path.isfile(filename):
        raise FileNotFoundError(
            f"The file, specified for uploading does not exist: {filename}"
        )

    file_url = return_json["links"]["html"]

    print(f"Uploading {file_name_to_upload} to Zenodo. This may take some time...")
    with open(filename, "rb") as fp:
        r = requests.put(f"{bucket_url}/{filebase}", data=fp, params=params)
        if r.status_code != 200:
            raise RuntimeError(f"The status code for the request is {r.status_code}.\nMessage: {r.text}")
        print(f"\nFile Uploaded successfully!\nFile link: {file_url}")

    print(f"Uploading {file_name_to_upload} metadata...")
    with open("configs/zenodo_metadata.yml") as fp:

        data = yaml.safe_load(fp)

        r = requests.put(
            f"{zenodo_server}/{deposition_id}",
            params=params,
            data=json.dumps(data),
            headers=headers,
        )
        if r.status_code != 200:
            raise RuntimeError(f"The status code for the request is {r.status_code}.\nMessage: {r.text}")

    print(f"Publishing {file_name_to_upload}...")
    r = requests.post(f"{zenodo_server}/{deposition_id}/actions/publish", params=params)
    if r.status_code != 202:
        raise RuntimeError(f"The status code for the request is {r.status_code}.\nMessage: {r.text}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=("Upload files to Zenodo."))
    parser.add_argument(
        "-f",
        "--file",
        dest="file_name_to_upload",
        help="path to the file to be uploaded",
    )
    args = parser.parse_args()
    upload_to_zenodo(args.file_name_to_upload)
