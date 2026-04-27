# LeadNurture AI — Automated Campaign Follow-Up Workflow

A Python-based automation tool that reads leads from Google Sheets, generates personalized B2B follow-up emails using AI, and updates the sheet status — ready to be sent via Zapier + Gmail.

---

## 📌 Overview

LeadNurture AI addresses the inefficiencies of manual follow-up in global talent outsourcing sales. Instead of copy-pasting emails and manually tracking leads, this workflow:

1. Reads new leads from a Google Sheet
2. Uses **Groq AI (LLaMA 3.1)** to generate a personalized follow-up email per lead
3. Writes the generated subject and body back into the sheet
4. Updates the lead status to `Email Generated`
5. Zapier then detects the status change and sends the email via Gmail

---

## 🗂️ Project Structure

```
leadnurture-ai/
├── venv                 # virtual environment
├── .env                 # Environment variables (do not share)
├── .gitignore           # Files ignored by git
├── credentials.json     # Google Service Account credentials (do not share)
├── export_workflow.py   # Zapier export json script
├── generate_email.py    # Main script
├── requirements.txt     # Python dependencies
└── README.md            # Project description
```

---

## ⚙️ Prerequisites

- Python 3.10+
- VS Code
- A Google account
- A Groq account (free) — [console.groq.com](https://console.groq.com)
- A Zapier account (free) — [zapier.com](https://zapier.com)
- Git 

---

## 🚀 Setup Guide

### 1. Clone or Download the Project
```bash
git clone https://github.com/daughpane05/leadnurture-ai.git
cd leadnurture-ai
```

### 2. Create and Activate a Virtual Environment
```bash
python -m venv venv

# Windows
venv\Scripts\activate

# Mac/Linux
source venv/bin/activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Set Up Google Sheets

Create a Google Sheet named **"LeadNurture AI"** with the following columns:

| A | B | C | D | E | F | G | H | I | J | K |
|---|---|---|---|---|---|---|---|---|---|---|
| Lead ID | First Name | Last Name | Company | Email | Country | Industry | Status | AI Email Subject | AI Email Body | Date Added |

Add dummy leads manually and set their `Status` to `New`.

Link for the Google Sheet used in this project: https://docs.google.com/spreadsheets/d/1n3rb8Uz0Un7kZCk6JWA0tKszUF8MKZdk2bRKdUp_KE8/edit?usp=drivesdk

### 5. Set Up Google Cloud Credentials

1. Go to [console.cloud.google.com](https://console.cloud.google.com)
2. Create a new project
3. Enable **Google Sheets API** and **Google Drive API**
4. Create a **Service Account** and download `credentials.json`
5. Place `credentials.json` in the project root folder
6. Share your Google Sheet with the service account email (Editor access)

### 6. Configure Environment Variables

Create a `.env` file in the project root:

```
GROQ_API_KEY=your-groq-api-key-here
SENDER_NAME=name-of-sender
SENDER_COMPANY=name-of-company
```

> Get your free Groq API key at [console.groq.com](https://console.groq.com) → API Keys → Create New Key
---

## ▶️ Running the Script

```bash
python generate_email.py
```

Expected output:
```
Processing: Full Name
Processing: Full Name
Processing: Full Name
Done processing all new leads.
```

After running, check your Google Sheet — leads with `Status = New` will be updated to `Email Generated` with AI-generated subject and body filled in columns I and J.

Manual script execution is used to enable controlled batch email delivery, reducing the risk of triggering spam detection systems.

---

## 🔁 Zapier Integration

Once the sheet is updated, Zapier handles sending the email automatically:

| Step | App | Action |
|---|---|---|
| Trigger | Google Sheets | New or Updated Row (Status column) |
| Filter | Zapier | Only continue if Status = `Email Generated` |
| Action 1 | Gmail | Send Email (To, Subject, Body from sheet) |
| Action 2 | Google Sheets | Update row Status to `Sent` |

---

## 🌐 Workflow Diagram

```
Google Sheets (Status = "New")
        ↓
generate_email.py
        ↓
Groq AI — LLaMA 3.1 (Generates personalized email)
        ↓
Google Sheets (Status → "Email Generated")
        ↓
Zapier (Detects status change)
        ↓
Gmail (Sends email)
        ↓
Google Sheets (Status → "Sent")
```

---

## 📦 Dependencies

```
gspread==6.1.2
google-auth==2.29.0
google-auth-oauthlib==1.2.0
google-auth-httplib2==0.2.0
python-dotenv==1.0.1
groq
```

---

## 🔒 Security Notes

- **Never commit** `.env` or `credentials.json` to version control
- Add both to your `.gitignore`:
```
.env
credentials.json
venv/
```

For this project, please contact the owner to access the .env and credentials.json files as these contain sensitive data.

---

## 🛠️ Tools Used

| Tool | Purpose | Cost |
|---|---|---|
| Python | Core scripting language | Free |
| Groq (LLaMA 3.1) | AI email generation | Free |
| Google Sheets | Lead database | Free |
| Google Cloud | Sheets API credentials | Free |
| Zapier | Workflow automation | Free tier |
| Gmail | Email delivery | Free |

---
