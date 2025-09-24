import os
import requests
import hashlib
from dotenv import load_dotenv

load_dotenv()

B2_KEY_ID = os.getenv("B2_KEY_ID")
B2_APPLICATION_KEY = os.getenv("B2_APPLICATION_KEY")
B2_BUCKET_ID = os.getenv("B2_BUCKET_ID")
B2_BUCKET_NAME = os.getenv("B2_BUCKET_NAME")

def b2_auth():
    auth_url = "https://api.backblazeb2.com/b2api/v2/b2_authorize_account"
    auth_response = requests.get(
        auth_url,
        auth=(B2_KEY_ID, B2_APPLICATION_KEY),
        timeout=20
    )
    return auth_response.json() if auth_response.status_code == 200 else None

def get_upload_url(auth_data):
    upload_url_response = requests.post(
        f"{auth_data['apiUrl']}/b2api/v2/b2_get_upload_url",
        json={"bucketId": B2_BUCKET_ID},
        headers={"Authorization": auth_data["authorizationToken"]},
        timeout=20
    )
    return upload_url_response.json() if upload_url_response.status_code == 200 else None

def upload_file(upload_url, upload_auth_token, file_name, file_content):
    file_sha1 = hashlib.sha1(file_content).hexdigest()
    upload_response = requests.post(
        upload_url,
        headers={
            "Authorization": upload_auth_token,
            "X-Bz-File-Name": file_name,
            "Content-Type": "application/octet-stream",
            "X-Bz-Content-Sha1": file_sha1,
        },
        data=file_content,
        timeout=30
    )
    return upload_response.status_code == 200

def list_files(auth_data):
    list_url = f"{auth_data['apiUrl']}/b2api/v2/b2_list_file_names"
    response = requests.post(
        list_url,
        json={"bucketId": B2_BUCKET_ID, "maxFileCount": 100},
        headers={"Authorization": auth_data["authorizationToken"]},
        timeout=20
    )
    return response.json()["files"] if response.status_code == 200 else []

def delete_file(auth_data, file_name):
    delete_url = f"{auth_data['apiUrl']}/b2api/v2/b2_delete_file_version"
    response = requests.post(
        delete_url,
        json={"fileName": file_name, "bucketId": B2_BUCKET_ID},
        headers={"Authorization": auth_data["authorizationToken"]},
        timeout=20
    )
    return response.status_code == 200

