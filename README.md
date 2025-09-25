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

