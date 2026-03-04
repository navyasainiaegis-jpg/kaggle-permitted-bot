from sheet_reader import fetch_emails
from kaggle_bot import add_emails_to_kaggle

emails = fetch_emails()
add_emails_to_kaggle(emails)
