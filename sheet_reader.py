import gspread
from oauth2client.service_account import ServiceAccountCredentials

def fetch_emails():
    scope = [
        "https://spreadsheets.google.com/feeds",
        "https://www.googleapis.com/auth/drive"
    ]

    creds = ServiceAccountCredentials.from_json_keyfile_name(
        "credentials.json", scope
    )

    client = gspread.authorize(creds)

    sheet = client.open("mails").sheet1

    records = sheet.get_all_records()

    emails = []

    for row in records:
        email = row.get("emailssss")
        if email:
            emails.append(email.strip())

    return list(set(emails))