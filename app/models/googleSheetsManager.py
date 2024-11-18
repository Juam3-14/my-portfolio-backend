import logging
import os
import gspread
from google.oauth2.service_account import Credentials

credentials_path = os.environ["GOOGLE_SHEETS_CREDENTIALS"]

class GoogleSheetsManager:
    def __init__(self):        
        scope = ["https://www.googleapis.com/auth/spreadsheets", "https://www.googleapis.com/auth/drive"]
        creds = Credentials.from_service_account_file(credentials_path, scopes=scope)
        self.client = gspread.authorize(creds)
        self.sheet = self.client.open_by_url(url="https://docs.google.com/spreadsheets/d/1qK6MDMP8ikNA87S_JeZZmsunUdzdrYujSPLSWr00x08/edit?usp=sharing")

    def save_contact_info(self, contact_info, id: str):
        try:
            self.sheet.get_worksheet(0).append_row([
                id,
                contact_info.firstName,
                contact_info.lastName,
                contact_info.email,
                contact_info.phone,
                contact_info.message
            ])
        except Exception as e: 
            logging.info(f"There was an error making the insertion of the message in gsheets: {e}")