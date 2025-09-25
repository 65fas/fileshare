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
fileshare/
├── .env                  # Environment variables
├── .gitignore            # Ignored files
├── README.md             # This file
├── b2_utils.py           # Backblaze B2 utility functions
├── backend/
│   ├── app.py            # Flask backend
│   └── requirements.txt  # Python dependencies
├── frontend/
│   ├── upload.html       # Upload page
│   ├── admin.html        # Admin page
│   └── static/           # Static files (CSS/JS)
├── render.yaml           # Render deployment config
└── test/                 # Test scripts
