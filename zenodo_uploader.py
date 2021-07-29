import os

import argparse
import requests
import traceback


def upload_to_zenodo(file_name_to_upload, zenodo_server="https://sandbox.zenodo.org/api/deposit/depositions"):
    headers = {"Content-Type": "application/json"}
    params = {"access_token": os.getenv("ZENODO_ACCESS_TOKEN", "")}
    r = requests.post(
        zenodo_server,
        params=params,
        json={},
        headers=headers,
    )
    return_json = r.json()
    deposition_id = return_json["id"]
    bucket_url = return_json["links"]["bucket"]
    filename = os.path.abspath(file_name_to_upload)
    if not os.path.isfile(filename):
        raise FileNotFoundError(f"The file, specified for uploading does not exist: {filename}")
    file_url = r.json()["links"]["html"]
    with open(filename, "rb") as fp:
        try:
            r = requests.put(f"{bucket_url}/{filename}", data=fp, params=params)
            print(
                f"\nFile Uploaded successfully!\nFile link: {file_url}"
            )
        except Exception as excinfo:
            print(
                f"\nFailed to upload file! Here is why:\n{''.join(traceback.format_exception(None, excinfo, excinfo.__traceback__))}"
            )
    r = requests.post(f"{zenodo_server}/{deposition_id}/actions/publish", params=params)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=("Upload files to Zenodo."))

    parser.add_argument(
        "-f", "--file", dest="file_name_to_upload", help="path to the file to be uploaded"
    )
    args = parser.parse_args()
    upload_to_zenodo(args.file_name_to_upload)
