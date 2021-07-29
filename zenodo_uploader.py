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
    #print(r.status_code)
    #print(r.json())
    bucket_url = r.json()["links"]["bucket"]
    filename = file_name_to_upload
    file_url = r.json()["links"]["html"]
    with open(filename, "rb") as fp:
        try:
            r = requests.put(f"{bucket_url}/{filename}", data=fp, params=params)
            print(
                f"\nFile Uploaded successfully!\nFile link: {file_url}"
            )
            print(r.status_code)
            print(r.json())
        except Exception as excinfo:
            print(
                f"\nFailed to upload file! Here is why:\n{''.join(traceback.format_exception(None, excinfo, excinfo.__traceback__))}"
            )
    r = requests.post(f"{zenodo_server}/{deposition_id}/actions/publish", params=params)
    #print(r.status_code)
    #print(r.json())


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=("Upload files to Zenodo."))

    parser.add_argument(
        "-f", "--file", dest="file_name_to_upload", help="the input config file"
    )
    args = parser.parse_args()
    upload_to_zenodo(args.file_name_to_upload)
