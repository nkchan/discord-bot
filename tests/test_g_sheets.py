# tests/test_g_sheets.py
import unittest
from unittest.mock import MagicMock, patch
import sys
import os

# Add the parent directory to the path to import the g_sheets module
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# Mock gspread library for CI environments where it might not be installed
if 'gspread' not in sys.modules:
    gspread = MagicMock()
    gspread.exceptions = MagicMock()
    gspread.exceptions.WorksheetNotFound = type('WorksheetNotFound', (Exception,), {})
    gspread.exceptions.CellNotFound = type('CellNotFound', (Exception,), {})
    sys.modules['gspread'] = gspread
    sys.modules['gspread.exceptions'] = gspread.exceptions

from g_sheets import GSheetsManager

class TestGSheetsManager(unittest.TestCase):

    @patch('sys.exit')
    @patch('g_sheets.ServiceAccountCredentials')
    @patch('g_sheets.gspread.authorize')
    def setUp(self, mock_authorize, mock_credentials, mock_exit):
        """
        Set up method executed before each test.
        Mocks gspread authentication and spreadsheet operations.
        """
        # Prevent sys.exit from being called during tests
        mock_exit.side_effect = SystemExit

        # Mock credentials loading
        mock_credentials.from_json_keyfile_name.return_value = MagicMock()

        # Mock gspread client
        self.mock_client = MagicMock()
        mock_authorize.return_value = self.mock_client

        self.mock_spreadsheet = MagicMock()
        self.mock_client.open_by_key.return_value = self.mock_spreadsheet

        self.manager = GSheetsManager('dummy_credentials.json', 'dummy_key')
        self.manager.spreadsheet = self.mock_spreadsheet  # Inject mock

    def test_get_or_create_sheet_existing(self):
        """
        Tests if an existing sheet is retrieved correctly.
        """
        mock_sheet = MagicMock()
        self.mock_spreadsheet.worksheet.return_value = mock_sheet

        sheet = self.manager._get_or_create_sheet("Books")

        self.mock_spreadsheet.worksheet.assert_called_with("Books")
        self.mock_spreadsheet.add_worksheet.assert_not_called()
        self.assertEqual(sheet, mock_sheet)

    def test_get_or_create_sheet_new(self):
        """
        Tests if a new sheet is created when it does not exist.
        """
        self.mock_spreadsheet.worksheet.side_effect = sys.modules['gspread'].exceptions.WorksheetNotFound
        new_mock_sheet = MagicMock()
        self.mock_spreadsheet.add_worksheet.return_value = new_mock_sheet

        sheet = self.manager._get_or_create_sheet("New Genre")

        self.mock_spreadsheet.worksheet.assert_called_with("New Genre")
        self.mock_spreadsheet.add_worksheet.assert_called_with(title="New Genre", rows="100", cols="20")
        # Verify that the header row is written in English
        new_mock_sheet.append_row.assert_called_with(["Title", "Status", "Added Date", "Completed Date"])
        self.assertEqual(sheet, new_mock_sheet)

    def test_add_item(self):
        """
        Tests if add_item calls the correct sheet and appends the correct data.
        """
        mock_sheet = MagicMock()
        with patch.object(self.manager, '_get_or_create_sheet', return_value=mock_sheet) as mock_get_sheet:
            result = self.manager.add_item("Books", "A New Book")

            mock_get_sheet.assert_called_with("Books")
            mock_sheet.append_row.assert_called_once()
            call_args = mock_sheet.append_row.call_args[0][0]
            self.assertEqual(call_args[0], "A New Book")
            self.assertEqual(call_args[1], "Pending") # Status should be Pending
            self.assertTrue(result)

if __name__ == '__main__':
    unittest.main()
