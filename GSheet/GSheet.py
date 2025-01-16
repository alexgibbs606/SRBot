import os.path
from pathlib import Path

import pandas as pd

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

# If modifying these scopes, delete the file token.json.
SRBOT_SCOPES = [
    'https://www.googleapis.com/auth/drive',
    'https://www.googleapis.com/auth/drive.file',
    'https://www.googleapis.com/auth/spreadsheets',
    'https://www.googleapis.com/auth/spreadsheets.readonly',
]
CREDS_PATH = Path().resolve() / 'creds'
GOOGLE_CREDS_FILE = CREDS_PATH / 'credentials.json'
TOKEN_FILEPATH = CREDS_PATH / 'token.json'

class GSheet():
    scopes = SRBOT_SCOPES

    def __init__(self, spreadsheet_id: str, selection_range: str, header: list=None, credentials_file: Path=None):
        self.spreadsheet_id = spreadsheet_id
        self.selection_range = selection_range

        self.creds = self._get_creds(credentials_file)
        self.service = build('sheets', 'v4', credentials=self.creds)
        self.sheet = self.service.spreadsheets() # pylint: disable=no-member

        self.header = header
        self.values = None

    def _get_creds(self, credentials_file: Path=None):
        creds = None
        # The file token.json stores the user's access and refresh tokens, and is
        # created automatically when the authorization flow completes for the first
        # time.
        # If we have a token.json file, we can use it to authenticate
        if os.path.exists(TOKEN_FILEPATH):
            creds = Credentials.from_authorized_user_file(TOKEN_FILEPATH, SRBOT_SCOPES)

        # If there are no (valid) credentials available, let the user log in.
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                # flow = service_account.Credentials.from_service_account_file(
                #     credentials_file, scopes=SCOPES
                # )
                flow = InstalledAppFlow.from_client_secrets_file(
                    credentials_file | GOOGLE_CREDS_FILE,
                    SRBOT_SCOPES,
                )
                creds = flow.run_local_server(port=0)
            # Save the credentials for the next run
            with open(TOKEN_FILEPATH, 'w', encoding='utf-8') as token:
                token.write(creds.to_json())

        return creds

    def __enter__(self, *args, **kwargs):
        # Collecting the values from the sheet in the given range
        values = self.sheet.values().get(
            spreadsheetId = self.spreadsheet_id,
            range = self.selection_range,
        ).execute().get('values', [])

        # Collecting header values if headers were not given
        if not self.header:
            self.header = values[0]
            self.values = pd.DataFrame(values[1:], columns=self.header)
        else:
            self.values = pd.DataFrame(values, columns=self.header)

        # Returning the object
        return self

    def __add__(self, data: dict):
        self.append(data)

    def __exit__(self, *_):
        pass

    def __len__(self):
        return len(self.values)


    # Pandas passthrough methods
    def loc(self, *args, **kwargs):
        if self.values is None:
            raise ValueError('No values have been gathered to locate.')
        return self.values.loc(*args, **kwargs)

    def __getitem__(self, *args, **kwargs):
        if self.values is None:
            raise ValueError('No values have been gathered to locate.')
        return self.values.__getitem__(*args, **kwargs)


    # Additional accessors and mutators
    def append(self, data: dict):
        ''' Appends a single row to the sheet.

        Args:
            data (dict): The data to add to the sheet. No required columns, but the column names must match the
                sheet's column names. Ordered by the header given in the constructor or the header of the sheet if no
                header was given.
        '''
        # Creating a new dictionary with all keys in lowercase and values as lists
        new_data = {
            key.lower(): value if isinstance(value, list) else [value]
            for key, value in data.items()
        }

        # Creating a DataFrame from the new dictionary to iterate through.
        data_pd = pd.DataFrame.from_dict(
            data = new_data,
            orient = 'columns',
        )
        for record in data_pd[[_.lower() for _ in self.header if _.lower() in data_pd.columns]].iterrows():
            record
            self.sheet.values().append(
                spreadsheetId=self.spreadsheet_id,
                range=self.selection_range,
                body={
                    'majorDimension': 'ROWS',
                    'values': [data[key.lower()] for key in self.header],
                },
                valueInputOption='USER_ENTERED'
            ).execute()


if __name__ == '__main__':
    with GSheet('1dViukl-IgpR1V-rqeG-7QVFBOHAyXnlgYDk5ZVi2ZFo', 'SRB!A:O') as sheet:
        print(sheet.values)