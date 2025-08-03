# g_sheets.py
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from datetime import datetime
import sys

# A class to manage operations with Google Sheets.
class GSheetsManager:
    def __init__(self, credentials_path, spreadsheet_key):
        """
        Connects to Google Sheets.
        """
        self.spreadsheet = None
        try:
            print("Attempting to authenticate with Google Sheets...")
            scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
            creds = ServiceAccountCredentials.from_json_keyfile_name(credentials_path, scope)
            self.client = gspread.authorize(creds)
            print("Authentication successful. Attempting to open spreadsheet...")
            self.spreadsheet = self.client.open_by_key(spreadsheet_key)
            print(f"Successfully opened spreadsheet: '{self.spreadsheet.title}'")
        except FileNotFoundError:
            print(f"!!! FATAL ERROR: Credentials file not found at '{credentials_path}'.")
            print("!!! Please ensure 'credentials.json' is in the project root directory.")
            sys.exit(1)
        except Exception as e:
            print(f"!!! FATAL ERROR during GSheetsManager initialization: {e}")
            print("!!! Please check your SPREADSHEET_KEY and ensure the service account has sharing permissions.")
            sys.exit(1)

    def _get_or_create_sheet(self, genre):
        """
        Gets a sheet by genre name, or creates it if it doesn't exist.
        """
        if not self.spreadsheet:
            return None
        try:
            print(f"Attempting to get worksheet: '{genre}'")
            sheet = self.spreadsheet.worksheet(genre)
            print(f"Found existing worksheet: '{genre}'")
            return sheet
        except gspread.exceptions.WorksheetNotFound:
            try:
                print(f"Worksheet '{genre}' not found. Attempting to create it...")
                sheet = self.spreadsheet.add_worksheet(title=genre, rows="100", cols="20")
                print(f"Successfully created worksheet: '{genre}'. Adding header row...")
                sheet.append_row(["Title", "Status", "Added Date", "Completed Date"])
                print("Header row added.")
                return sheet
            except Exception as e:
                print(f"!!! ERROR creating new worksheet '{genre}': {e}")
                return None
        except Exception as e:
            print(f"!!! ERROR in _get_or_create_sheet for genre '{genre}': {e}")
            return None

    def add_item(self, genre, title):
        """
        Adds a new item to the sheet corresponding to the genre.
        """
        try:
            sheet = self._get_or_create_sheet(genre)
            if sheet is None:
                return False
            today = datetime.now().strftime('%Y-%m-%d')
            new_row = [title, 'Pending', today, '']
            print(f"Appending row to '{genre}': {new_row}")
            sheet.append_row(new_row)
            print("Row appended successfully.")
            return True
        except Exception as e:
            print(f"!!! ERROR in add_item: {e}")
            return False

    def mark_as_done(self, genre, title):
        """
        Updates the status of an item to "Completed".
        """
        try:
            sheet = self._get_or_create_sheet(genre)
            if sheet is None:
                return False
            print(f"Searching for '{title}' in '{genre}' to mark as done...")
            cell = sheet.find(title)
            row_index = cell.row
            today = datetime.now().strftime('%Y-%m-%d')
            sheet.update_cell(row_index, 2, 'Completed')
            sheet.update_cell(row_index, 4, today)
            print(f"Successfully marked '{title}' as completed.")
            return True
        except gspread.exceptions.CellNotFound:
            print(f"Could not find cell with title '{title}' in sheet '{genre}'.")
            return False
        except Exception as e:
            print(f"!!! ERROR in mark_as_done: {e}")
            return False

    def get_list(self, genre):
        """
        Retrieves a list of items for a given genre.
        """
        try:
            sheet = self._get_or_create_sheet(genre)
            if sheet is None:
                return None # Indicate error
            print(f"Fetching all records from '{genre}'...")
            records = sheet.get_all_records()
            print(f"Found {len(records)} records.")
            return records
        except Exception as e:
            print(f"!!! ERROR in get_list: {e}")
            return None
