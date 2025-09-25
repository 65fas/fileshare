# FileShare: Secure File Upload with Backblaze B2

A **minimal, secure file-sharing app** built with **Flask (Python)** and **Backblaze B2** for storage.
Users can upload files via a web interface, and admins can manage files with token-based access control and rate limiting. Link: https://fileshare-8201.onrender.com/

---

## **Key Features**
### **Frontend**
- **Upload Page**: Simple drag-and-drop interface for file uploads.
- **Admin Page**: List and delete files (protected by token).
- **Responsive Design**: Works on mobile and desktop.

### **Backend**
- **Token-Based Access**: Only pre-defined tokens allow uploads.
- **Rate Limiting**: 10 uploads/hour per token/IP to prevent abuse.
- **Backblaze B2 Integration**: Files are stored securely in your B2 bucket.

---

## **Project Structure**
```text
fileshare/
├── .env                  # Environment variables
├── .gitignore            # Ignored files
├── README.md             # Project documentation
├── b2_utils.py           # Backblaze B2 utility functions
├── backend/
│   ├── app.py            # Flask backend logic
│   └── requirements.txt  # Python dependencies
├── frontend/
│   ├── upload.html       # File upload interface
│   ├── admin.html        # Admin panel
│   └── static/           # Static assets (CSS/JS)
├── render.yaml           # Render deployment configuration
└── test/
    ├── test-b2.py        # Backblaze B2 test script
    ├── download_latest_file.py  # Download latest file script
    └── download/         # Downloaded files
```

---

## Setup Instructions

```bash
# 1. Clone the Repository
git clone https://github.com/yourusername/fileshare.git
cd fileshare

# 2. Install Dependencies
pip install -r backend/requirements.txt

# 3. Configure Environment Variables
# Create a `.env` file in the root directory with:
# ----------------------------
# B2_KEY_ID=your_backblaze_key_id
# B2_APPLICATION_KEY=your_backblaze_application_key
# B2_BUCKET_ID=your_backblaze_bucket_id
# B2_BUCKET_NAME=your_backblaze_bucket_name
# VALID_TOKENS=abc123,xyz789,test123
# FLASK_ENV=development
# ----------------------------

# 4. Run Locally
flask run

# Access the app at:
# Upload Page: http://localhost:5000/upload/abc123
# Admin Panel: http://localhost:5000/admin

# 5. Deploy to Render
# Push to GitHub:
git add .
git commit -m "Ready for deployment"
git push origin main

# Render Configuration:
# ----------------------------
# Build Command: pip install -r backend/requirements.txt
# Start Command: gunicorn --bind 0.0.0.0:10000 backend.app\:app
# Environment Variables:
#   B2_KEY_ID=your_backblaze_key_id
#   B2_APPLICATION_KEY=your_backblaze_application_key
#   B2_BUCKET_ID=your_backblaze_bucket_id
#   B2_BUCKET_NAME=your_backblaze_bucket_name
#   VALID_TOKENS=abc123,xyz789,test123
#   FLASK_ENV=production
#   PYTHONPATH=/opt/render/project/src
# ----------------------------

# 6. Test Deployment
# Open your Render URL (e.g., https://your-app.onrender.com/upload/abc123)
# Verify uploads and admin features work
