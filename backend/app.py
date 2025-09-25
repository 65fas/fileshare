from flask import Flask, request, send_from_directory, jsonify
from werkzeug.utils import secure_filename
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from b2_utils import b2_auth, get_upload_url, upload_file, list_files, delete_file
import os

app = Flask(__name__, static_folder='../frontend/static')

# Rate limiter setup
limiter = Limiter(
    app=app,
    key_func=get_remote_address,  # Limits by IP address
    default_limits=["10 per hour"]  # Default rate limit
)

# Valid tokens (manually defined)
VALID_TOKENS = set(os.getenv("VALID_TOKENS", "").split(","))

# Serve frontend files
@app.route('/')
def index():
    return send_from_directory('../frontend', 'upload.html')

@app.route('/upload/<upload_id>', methods=['GET'])
def upload_page(upload_id):
    return send_from_directory('../frontend', 'upload.html')

@app.route('/admin', methods=['GET'])
def admin_page():
    return send_from_directory('../frontend', 'admin.html')

# Handle file upload with token validation and rate limiting
@app.route('/api/upload/<upload_id>', methods=['POST'])
@limiter.limit("10 per hour")  # Rate limit for this endpoint
def handle_upload(upload_id):
    # Validate token
    if upload_id not in VALID_TOKENS:
        return 'Invalid token.', 403

    if 'file' not in request.files:
        return 'No file uploaded.', 400

    file = request.files['file']
    if file.filename == '':
        return 'No file selected.', 400

    auth_data = b2_auth()
    if not auth_data:
        return 'Failed to authorize with Backblaze B2.', 500

    upload_data = get_upload_url(auth_data)
    if not upload_data:
        return 'Failed to get upload URL.', 500

    file_content = file.read()
    success = upload_file(
        upload_data["uploadUrl"],
        upload_data["authorizationToken"],
        f"{upload_id}_{secure_filename(file.filename)}",
        file_content
    )

    return 'File uploaded successfully!' if success else 'Failed to upload file.', 500

# List files (protected by token if needed)
@app.route('/api/files', methods=['GET'])
def files():
    auth_data = b2_auth()
    if not auth_data:
        return jsonify([]), 500

    files = list_files(auth_data)
    return jsonify(files)

# Delete a file (protected by token if needed)
@app.route('/api/files/<file_name>', methods=['DELETE'])
def delete(file_name):
    auth_data = b2_auth()
    if not auth_data:
        return 'Failed to authorize with Backblaze B2.', 500

    success = delete_file(auth_data, file_name)
    return 'File deleted.' if success else 'Failed to delete file.', 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000) 

