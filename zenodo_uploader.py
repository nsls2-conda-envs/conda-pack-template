import argparse
import json
import os

import requests
import yaml
import json
from urllib.parse import urlencode
import traceback

def search_for_deposition(
    title,
    owner=None,
    zenodo_server="https://sandbox.zenodo.org/api/",
):
    print(f"Searching for depositions...\n")
    search = f'metadata.title:"{title}"'
    if owner:
        search += f" owners:{owner}"

    search = search.replace("/", " ")  # zenodo can't handle '/' in search query

    params = {"q": search, "sort": "mostrecent"}
    url = zenodo_server + "deposit/depositions?" + urlencode(params)

    try:
        response = requests.get(url).json()
        records = [hit for hit in response["hits"]["hits"]]
    except Exception as excinfo:
        print("No title matches found! here is What happened:\n")
        traceback.format_exc()
        return None, None, None

    if not records:
        print(f"No records found for search: '{title}'")
        return None, None, None

    print(f"Found `{len(records)}` depositions!")
    
    depositions = []
    for deposition in records:
        if deposition["metadata"]["title"] == title or deposition["owner"] == owner:
            depositions.append(deposition)

    if not depositions:
        print(f"No records found for search: '{title}'")
        return None, None, None

    deposition = sorted(
        depositions,
        key=lambda deposition: deposition["metadata"]["publication_date"],
        reverse=True,
    )[0]

    print(f"Best match is deposition: {deposition['id']}")
    return (
        deposition["id"],
        deposition["links"]["bucket"],
        deposition["links"]["html"].replace("deposit", "record"),
    )

def create_new_version(
    deposition_id, token, zenodo_server="https://sandbox.zenodo.org/api/"
):
    url = f"{zenodo_server}deposit/depositions/{deposition_id}/actions/newversion"
    r = requests.post(
        url,
        params={"access_token": token},
    )
    r.raise_for_status()

    deposition = r.json()
    new_deposition_url = deposition["links"]["latest_draft"]
    new_deposition_id = new_deposition_url.split("/")[-1]

    r = requests.get(
        f"{zenodo_server}deposit/depositions/{new_deposition_id}",
           params={"access_token": token},
    )
    r.raise_for_status()
    deposition = r.json()

    return (
        deposition["id"],
        deposition["links"]["bucket"],
        deposition["links"]["html"].replace("deposit", "record"),
    )

def create_new_deposition(token, zenodo_server="https://sandbox.zenodo.org/api/"):
    url = f"{zenodo_server}deposit/depositions"
    r = requests.post(
        url,
        params={"access_token": token},
        json={},
        headers={"Content-Type": "application/json"},
    )
    r.raise_for_status()

    deposition = r.json()

    return (
        deposition["id"],
        deposition["links"]["bucket"],
        deposition["links"]["html"].replace("deposit", "record"),
    )

def upload_to_zenodo(
    deposition_id,
    filename,
    bucket_url,
    file_url,
    filebase,
    env_name,
    token,
    zenodo_server="https://sandbox.zenodo.org/api/",
):
    if filename.endswith(".tar.gz"):
        response = requests.get(
            f"{zenodo_server}deposit/depositions/{deposition_id}",
            params={"access_token": token},
            headers={"Content-Type": "application/json"},
        )
        response.raise_for_status()

        print(f"Comparing {filename} checksum with files on zenodo...")
        files_checksums = [file["checksum"] for file in response.json()["files"]]
        with open(f"{env_name}-md5sum.txt", "r") as fp:
            content = fp.read()
            current_file_checksum = content.split("=")[-1].strip()

        if current_file_checksum in files_checksums:
            print(f"File: {filename} is already uploaded!\n")
            return
        else:
            print(f"No conflicting files!\n")

    print(f"Uploading {filename} to Zenodo. This may take some time...")
    with open(filename, "rb") as fp:
        r = requests.put(
            f"{bucket_url}/{filebase}", data=fp, params={"access_token": token}
        )
        r.raise_for_status()
        print(f"\nFile Uploaded successfully!\nFile link: {file_url}")

def add_meta_data(
    deposition_id,
    meta_data,
    token,
    zenodo_server="https://sandbox.zenodo.org/api/",
):
    print(f"Uploading metadata for {filename} ...")

    r = requests.put(
        f"{zenodo_server}deposit/depositions/{deposition_id}",
        params={"access_token": token},
        data=json.dumps(meta_data),
        headers={"Content-Type": "application/json"},
    )

    r.raise_for_status()

def publish_file(
    deposition_id,
    token,
    zenodo_server="https://sandbox.zenodo.org/api/",
):
    print(f"Publishing deposition: {deposition_id}...")
    r = requests.post(
        f"{zenodo_server}deposit/depositions/{deposition_id}/actions/publish",
        params={"access_token": token},
    )

    r.raise_for_status()

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=("Upload files to Zenodo."))
    parser.add_argument(
        "-f",
        "--file",
        dest="files_to_upload",
        help="path to the file to be uploaded",
        required=True,
        action="append",
    )
    parser.add_argument(
        "-c",
        "--config-file",
        dest="config_file",
        help="config file with metadata information",
        required=True,
    )
    parser.add_argument(
        "-p",
        "--publish",
        dest="publish",
        action="store_true",
        help="Whether to publish file or not",
    )
    args = parser.parse_args()

    token = os.getenv("ZENODO_ACCESS_TOKEN")
    if not token:
        exit(
            "No access token provided!\n"
            "Please create an environment variable with the token.\n"
            "Variable Name: `ZENODO_ACCESS_TOKEN`"
        )

    config_file = os.path.abspath(args.config_file)
    if not os.path.isfile(config_file):
        raise FileNotFoundError(
            f"The file with metadata, specified for uploading does not exist: {config_file}"
        )

    with open(config_file) as fp:
        try:
            content = yaml.safe_load(fp)
            meta_data = content["zenodo_metadata"]
            env_name = content["env_name"]
        except:
            exit(f"Please add metadata to the config file: {config_file}")

    deposition_id, bucket_url, file_url = search_for_deposition(
        title=meta_data["metadata"]["title"],
        owner=int(os.getenv("ZENODO_OWNER_ID")),
    )

    if not deposition_id:
        deposition_id, bucket_url, file_url = create_new_deposition(token=token)

        for file in args.files_to_upload:
            filename = os.path.abspath(file)
            filebase = os.path.basename(filename)
            if not os.path.isfile(filename):
                raise FileNotFoundError(
                    f"The file, specified for uploading does not exist or is a directory: {filename}"
                )

            upload_to_zenodo(
                deposition_id=deposition_id,
                filename=file,
                bucket_url=bucket_url,
                file_url=file_url,
                filebase=filebase,
                token=token,
                env_name=env_name
            )
            add_meta_data(
                deposition_id=deposition_id,
                meta_data=meta_data,
                token=token,
            )

        if args.publish:
            publish_file(deposition_id=deposition_id, token=token)
    else:
        for file in args.files_to_upload:
            filename = os.path.abspath(file)
            filebase = os.path.basename(filename)
            if not os.path.isfile(filename):
                raise FileNotFoundError(
                    f"The file, specified for uploading does not exist or is a directory: {filename}"
                )

            deposition_id, bucket_url, file_url = create_new_version(
                deposition_id=deposition_id,
                token=token,
            )
            upload_to_zenodo(
                deposition_id=deposition_id,
                filename=file,
                bucket_url=bucket_url,
                file_url=file_url,
                filebase=filebase,
                env_name=env_name,
                token=token,
            )
        if args.publish:
            publish_file(deposition_id=deposition_id, token=token)
