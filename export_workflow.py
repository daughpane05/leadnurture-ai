import gspread
from google.oauth2.service_account import Credentials
from dotenv import load_dotenv
import os
import json
from datetime import datetime

load_dotenv()

# ── CONFIG ──────────────────────────────────────────────
SPREADSHEET_NAME = "LeadNurture AI"
SENDER_NAME      = os.getenv("SENDER_NAME")
SENDER_COMPANY   = os.getenv("SENDER_COMPANY")
# ────────────────────────────────────────────────────────

# Connect to Google Sheets
scopes = ["https://www.googleapis.com/auth/spreadsheets",
          "https://www.googleapis.com/auth/drive"]
creds  = Credentials.from_service_account_file("credentials.json", scopes=scopes)
gc     = gspread.authorize(creds)
sheet  = gc.open(SPREADSHEET_NAME).sheet1

def export_workflow():
    records = sheet.get_all_records()

    # Build processed leads list from sheet
    processed_leads = []
    for row in records:
        if row.get("Status") in ["Email Generated", "Sent"]:
            processed_leads.append({
                "lead_id":    row.get("Lead ID"),
                "name":       f"{row.get('First Name')} {row.get('Last Name')}",
                "company":    row.get("Company"),
                "email":      row.get("Email"),
                "country":    row.get("Country"),
                "industry":   row.get("Industry"),
                "status":     row.get("Status"),
                "ai_subject": row.get("AI Email Subject"),
                "ai_body":    row.get("AI Email Body"),
            })

    workflow = {
        "workflow_name": "LeadNurture AI — Automated Campaign Follow-Up",
        "exported_at": datetime.now().isoformat(),
        "description": "Automated B2B follow-up email workflow for global talent outsourcing leads.",
        "tools": {
            "ai_model":     "Groq — LLaMA 3.1 (llama-3.1-8b-instant)",
            "database":     "Google Sheets",
            "automation":   "Zapier",
            "email":        "Gmail",
            "language":     "Python 3.12"
        },
        "zapier_zap": {
            "zap_name": "LeadNurture AI — Send Follow-Up Email",
            "steps": [
                {
                    "step": 1,
                    "type": "Trigger",
                    "app": "Google Sheets",
                    "action": "New or Updated Spreadsheet Row",
                    "config": {
                        "spreadsheet": SPREADSHEET_NAME,
                        "worksheet":   "Sheet1",
                        "trigger_column": "H (Status)"
                    }
                },
                {
                    "step": 2,
                    "type": "Filter",
                    "app": "Zapier Filter",
                    "action": "Only continue if",
                    "config": {
                        "field":    "Status",
                        "condition": "equals",
                        "value":    "Email Generated"
                    }
                },
                {
                    "step": 3,
                    "type": "Action",
                    "app": "Gmail",
                    "action": "Send Email",
                    "config": {
                        "to":      "{{Email}} — Column E",
                        "subject": "{{AI Email Subject}} — Column I",
                        "body":    "{{AI Email Body}} — Column J",
                        "from_name": SENDER_NAME,
                        "company":   SENDER_COMPANY
                    }
                },
                {
                    "step": 4,
                    "type": "Action",
                    "app": "Google Sheets",
                    "action": "Update Spreadsheet Row",
                    "config": {
                        "spreadsheet": SPREADSHEET_NAME,
                        "worksheet":   "Sheet1",
                        "column_H":    "Sent"
                    }
                }
            ]
        },
        "python_script": {
            "file":        "email_generator.py",
            "ai_provider": "Groq",
            "model":       "llama-3.1-8b-instant",
            "functions": [
                "generate_email() — Calls Groq AI to generate personalized email",
                "process_leads() — Reads leads from Google Sheets and updates status"
            ]
        },
        "test_run_results": {
            "total_leads_processed": len(processed_leads),
            "leads": processed_leads
        }
    }

    with open("zapier_workflow.json", "w", encoding="utf-8") as f:
        json.dump(workflow, f, indent=4, ensure_ascii=False)

    print(f"Workflow exported successfully — {len(processed_leads)} leads included.")
    print("File saved: zapier_workflow.json")

if __name__ == "__main__":
    export_workflow()