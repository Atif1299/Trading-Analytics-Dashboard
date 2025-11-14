"""
Google Sheets Sync Service
Simple and clean implementation for syncing trading data
"""
import gspread
from google.oauth2.service_account import Credentials
import pandas as pd
from typing import List, Dict
import os
from datetime import datetime


class GoogleSheetsSync:
    """Handles all Google Sheets operations - super simple!"""
    
    def __init__(self, credentials_file: str):
        """Initialize with Google credentials"""
        self.credentials_file = credentials_file
        self.client = None
        self.last_sync = None
        self._authenticate()
    
    def _authenticate(self):
        """Authenticate with Google Sheets API"""
        try:
            # Define the scope
            scopes = [
                'https://www.googleapis.com/auth/spreadsheets.readonly',
                'https://www.googleapis.com/auth/drive.readonly'
            ]
            
            # Load credentials
            creds = Credentials.from_service_account_file(
                self.credentials_file, 
                scopes=scopes
            )
            self.client = gspread.authorize(creds)
            print("✅ Successfully authenticated with Google Sheets")
            
        except Exception as e:
            print(f"❌ Authentication failed: {str(e)}")
            raise
    
    def fetch_sheet_data(self, sheet_id: str, worksheet_name: str = None, worksheet_gid: str = None) -> List[Dict]:
        """
        Fetch data from a Google Sheet
        
        Args:
            sheet_id: The Google Sheet ID (from the URL)
            worksheet_name: Specific worksheet name (optional)
            worksheet_gid: Worksheet GID (optional, takes precedence over worksheet_name)
        
        Returns:
            List of dictionaries containing stock data
        """
        try:
            # Open the spreadsheet
            spreadsheet = self.client.open_by_key(sheet_id)
            
            # Get the worksheet
            if worksheet_gid:
                # Find worksheet by GID
                worksheet = None
                for ws in spreadsheet.worksheets():
                    if str(ws.id) == str(worksheet_gid):
                        worksheet = ws
                        print(f"📄 Using worksheet with GID: {worksheet_gid} ('{ws.title}')")
                        break
                if not worksheet:
                    print(f"⚠️ Warning: GID {worksheet_gid} not found, using first sheet")
                    worksheet = spreadsheet.get_worksheet(0)
            elif worksheet_name:
                worksheet = spreadsheet.worksheet(worksheet_name)
                print(f"📄 Using worksheet: '{worksheet_name}'")
            else:
                worksheet = spreadsheet.get_worksheet(0)
                print(f"📄 Using first worksheet: '{worksheet.title}'")
            
            # Get all records as list of dictionaries
            records = worksheet.get_all_records()
            
            # Update last sync time
            self.last_sync = datetime.now()
            
            print(f"✅ Fetched {len(records)} records from sheet")
            return records
            
        except Exception as e:
            print(f"❌ Error fetching sheet data: {str(e)}")
            raise
    
    def fetch_multiple_sheets(self, sheet_ids: List[str]) -> Dict[str, List[Dict]]:
        """
        Fetch data from multiple sheets
        
        Args:
            sheet_ids: List of Google Sheet IDs
        
        Returns:
            Dictionary with sheet_id as key and data as value
        """
        all_data = {}
        
        for sheet_id in sheet_ids:
            try:
                data = self.fetch_sheet_data(sheet_id)
                all_data[sheet_id] = data
            except Exception as e:
                print(f"⚠️ Failed to fetch sheet {sheet_id}: {str(e)}")
                all_data[sheet_id] = []
        
        return all_data
    
    def get_sheet_info(self, sheet_id: str) -> Dict:
        """Get metadata about a sheet"""
        try:
            spreadsheet = self.client.open_by_key(sheet_id)
            
            return {
                "title": spreadsheet.title,
                "worksheets": [ws.title for ws in spreadsheet.worksheets()],
                "last_updated": spreadsheet.lastUpdateTime if hasattr(spreadsheet, 'lastUpdateTime') else None
            }
            
        except Exception as e:
            print(f"❌ Error getting sheet info: {str(e)}")
            return {}


# Simple helper function to convert sheet data to pandas DataFrame
def to_dataframe(data: List[Dict]) -> pd.DataFrame:
    """Convert sheet data to pandas DataFrame for easy analysis"""
    if not data:
        return pd.DataFrame()
    
    df = pd.DataFrame(data)
    
    # Clean up column names (remove extra spaces)
    df.columns = df.columns.str.strip()
    
    return df
