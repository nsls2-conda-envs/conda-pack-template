import requests
import os
os.getenv('ZENODO_ACCESS_TOKEN: ')
headers = {"Content-Type": "application/json"}
params = {'access_token': ACCESS_TOKEN}
r = requests.post('https://sandbox.zenodo.org/api/deposit/depositions', params=params, json={}, headers=headers)
bucket_url = r.json()["links"]["bucket"]
filename = input("Enter filename as 'my-file.zip': ")
path = input("Enter file path as '/path/to/my-file.zip': ")
print("Hold on. This will take a while...")
with open(path, "rb") as fp:
    r = requests.put(
        "f"(bucket_url, filename),
        data=fp,
        params=params
    )
