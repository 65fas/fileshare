# test/download_latest_file.py
import os
import requests
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Backblaze B2 credentials
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

    if auth_response.status_code == 200:
        print("✅ B2 Authorization Successful!")
        return auth_response.json()
    else:
        print(f"❌ B2 Authorization Failed: {auth_response.status_code}")
        print(f"Response: {auth_response.text}")
        return None

def list_files(auth_data):
    list_url = f"{auth_data['apiUrl']}/b2api/v2/b2_list_file_names"
    response = requests.post(
        list_url,
        json={"bucketId": B2_BUCKET_ID, "maxFileCount": 100},
        headers={"Authorization": auth_data["authorizationToken"]},
        timeout=20
    )

    if response.status_code == 200:
        files = response.json()["files"]
        if not files:
            print("No files found in the bucket.")
            return None
        # Sort files by uploadTimestamp (newest first)
        files.sort(key=lambda x: x["uploadTimestamp"], reverse=True)
        latest_file = files[0]
        print(f"Latest file: {latest_file['fileName']} (ID: {latest_file['fileId']})")
        return latest_file
    else:
        print(f"Failed to list files: {response.text}")
        return None

def generate_presigned_url(auth_data, file_name):
    download_url = f"{auth_data['apiUrl']}/b2api/v2/b2_get_download_authorization"
    download_auth_response = requests.get(
        download_url,
        params={
            "bucketId": B2_BUCKET_ID,
            "fileNamePrefix": file_name,
            "validDurationInSeconds": 3600  # URL valid for 1 hour
        },
        headers={"Authorization": auth_data["authorizationToken"]},
        timeout=20
    )

    if download_auth_response.status_code == 200:
        download_auth_data = download_auth_response.json()
        presigned_url = f"{auth_data['downloadUrl']}/file/{B2_BUCKET_NAME}/{file_name}?Authorization={download_auth_data['authorizationToken']}"
        print(f"Pre-signed URL: {presigned_url}")
        return presigned_url
    else:
        print(f"Failed to generate pre-signed URL: {download_auth_response.text}")
        return None

def download_file(presigned_url, file_name):
    download_response = requests.get(presigned_url, timeout=20)

    if download_response.status_code == 200:
        # Create the 'test/download' folder if it doesn't exist
        download_dir = os.path.join(os.path.dirname(__file__), "download")
        if not os.path.exists(download_dir):
            os.makedirs(download_dir)

        # Save the file to the 'test/download' folder
        file_path = os.path.join(download_dir, file_name)
        with open(file_path, "wb") as f:
            f.write(download_response.content)

        print(f"✅ Downloaded file saved to: {file_path}")
    else:
        print(f"❌ Failed to download file: {download_response.text}")

if __name__ == "__main__":
    auth_data = b2_auth()
    if auth_data:
        latest_file = list_files(auth_data)
        if latest_file:
            presigned_url = generate_presigned_url(auth_data, latest_file["fileName"])
            if presigned_url:
                download_file(presigned_url, latest_file["fileName"])

