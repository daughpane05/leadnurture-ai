import gspread
from google.oauth2.service_account import Credentials
from dotenv import load_dotenv
from groq import Groq
import os
import time

load_dotenv()

# ── CONFIG ──────────────────────────────────────────────
SPREADSHEET_NAME = "LeadNurture AI"
GROQ_API_KEY     = os.getenv("GROQ_API_KEY")
SENDER_NAME      = os.getenv("SENDER_NAME")
SENDER_COMPANY   = os.getenv("SENDER_COMPANY")
# ────────────────────────────────────────────────────────

# Configure Groq
client = Groq(api_key=GROQ_API_KEY)

# Connect to Google Sheets
scopes = ["https://www.googleapis.com/auth/spreadsheets",
          "https://www.googleapis.com/auth/drive"]
creds  = Credentials.from_service_account_file("credentials.json", scopes=scopes)
gc     = gspread.authorize(creds)
sheet  = gc.open(SPREADSHEET_NAME).sheet1

def generate_email(lead: dict) -> tuple[str, str]:
    prompt = f"""
    You are a professional B2B sales representative for a global talent outsourcing company.
    Write a short, personalized cold follow-up email for this lead:
    
    - Name: {lead['first_name']} {lead['last_name']}
    - Company: {lead['company']}
    - Country: {lead['country']}
    - Industry: {lead['industry']}
    
    The email should:
    1. Be friendly and concise (under 150 words) but also professional
    2. Mention how outsourcing talent from the Philippines can benefit their {lead['industry']} business
    3. End with a clear call-to-action to book a discovery call
    4. Ensure that the calendar link is included for easy booking
    5. Always sign off with:
       Best regards,
       {SENDER_NAME}
       {SENDER_COMPANY}
    
    Return ONLY in this format:
    SUBJECT: <subject line>
    BODY: <email body>
    """
    response = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=[{"role": "user", "content": prompt}]
    )
    text    = response.choices[0].message.content.strip()
    subject = text.split("SUBJECT:")[1].split("BODY:")[0].strip()
    body    = text.split("BODY:")[1].strip()
    return subject, body

def process_leads():
    records = sheet.get_all_records()
    for i, row in enumerate(records, start=2):
        if row.get("Status") == "New":
            print(f"Processing: {row['First Name']} {row['Last Name']}")
            subject, body = generate_email({
                "first_name": row["First Name"],
                "last_name":  row["Last Name"],
                "company":    row["Company"],
                "country":    row["Country"],
                "industry":   row["Industry"],
            })
            sheet.update_cell(i, 9,  subject)
            sheet.update_cell(i, 10, body)
            sheet.update_cell(i, 8,  "Email Generated")
            time.sleep(3)

    print("Done processing all new leads.")

if __name__ == "__main__":
    process_leads()