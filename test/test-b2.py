import os
import requests
import hashlib
from dotenv import load_dotenv

load_dotenv()

B2_KEY_ID = os.getenv("B2_KEY_ID")
B2_APPLICATION_KEY = os.getenv("B2_APPLICATION_KEY")
B2_BUCKET_ID = os.getenv("B2_BUCKET_ID")
B2_BUCKET_NAME = os.getenv("B2_BUCKET_NAME")

def test_b2_auth():
    auth_url = "https://api.backblazeb2.com/b2api/v2/b2_authorize_account"
    auth_response = requests.get(
        auth_url,
        auth=(B2_KEY_ID, B2_APPLICATION_KEY),
        timeout=20
    )

    if auth_response.status_code == 200:
        print("✅ B2 Authorization Successful!")
        auth_data = auth_response.json()
        print(f"Account ID: {auth_data['accountId']}")
        return auth_data
    else:
        print(f"❌ B2 Authorization Failed: {auth_response.status_code}")
        print(f"Response: {auth_response.text}")
        return None

def test_b2_upload(auth_data):
    upload_url_response = requests.post(
        f"{auth_data['apiUrl']}/b2api/v2/b2_get_upload_url",
        json={"bucketId": B2_BUCKET_ID},
        headers={"Authorization": auth_data["authorizationToken"]},
        timeout=20
    )

    if upload_url_response.status_code != 200:
        print(f"❌ Failed to get upload URL: {upload_url_response.text}")
        return None

    upload_data = upload_url_response.json()
    upload_url = upload_data["uploadUrl"]
    upload_auth_token = upload_data["authorizationToken"]

    test_file = b"This is a test file."
    file_sha1 = hashlib.sha1(test_file).hexdigest()

    upload_response = requests.post(
        upload_url,
        headers={
            "Authorization": upload_auth_token,
            "X-Bz-File-Name": "test_upload.txt",
            "Content-Type": "text/plain",
            "X-Bz-Content-Sha1": file_sha1,
        },
        data=test_file,
        timeout=30
    )

    if upload_response.status_code == 200:
        print("✅ File uploaded successfully!")
        return upload_data
    else:
        print(f"❌ Upload failed: {upload_response.status_code}")
        print(f"Response: {upload_response.text}")
        return None

if __name__ == "__main__":
    auth_data = test_b2_auth()
    if auth_data:
        test_b2_upload(auth_data)

