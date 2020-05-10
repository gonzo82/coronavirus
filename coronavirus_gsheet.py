from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from datetime import datetime
import datetime
import os
import pickle

from coronavirus_database import Database


class Gsheet:

    services = {}
    database = Database()
    filename = 'coronavirus_data'
    file_id = ''
    increment = 10000

    def gsheet_service(self):
        """
        Esta función devuelve los 2 servicios necesarios de google en un diccionario:
             - sheets service
             - drive service
        """
        scopes = [
            'https://www.googleapis.com/auth/spreadsheets',
            'https://www.googleapis.com/auth/drive.file',
            'https://www.googleapis.com/auth/drive'
        ]
        creds = None

        if os.path.exists('token.pickle'):
            with open('token.pickle', 'rb') as token:
                creds = pickle.load(token)
        # If there are no (valid) credentials available, let the user log in.
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file('credentials.json', scopes)
                creds = flow.run_local_server(port=0)
            # Save the credentials for the next run
            with open('token.pickle', 'wb') as token:
                pickle.dump(creds, token)

        service_sheet = build('sheets', 'v4', credentials=creds)
        service_drive = build('drive', 'v3', credentials=creds)
        self.services = {
            'sheet': service_sheet,
            'drive': service_drive
        }

        return

    def get_gdrive_file_id(self):
        """
        Esta función devuelve el id de un fichero de drive desde su nombre
        """
        files = self.services['drive'].files()
        results = files.list(q="trashed=false and name='{}'".format(self.filename), fields="files(id)").execute()
        items = results.get('files', [])
        try:
            self.file_id = items[0]['id']
        except:
            file_metadata = {
                'name': self.filename,
                'mimeType': 'application/vnd.google-apps.spreadsheet'
            }
            file = files.create(body=file_metadata, fields='id').execute()
            self.file_id = file.get('id')
        return

    def upload_gsheet_data(self, gsheet_list, sheet):
        """
        Esta función carga los datos de una lista dentro de un gsheet.
        Lo hago en bloques, porque de 1 en uno es muy lento y todo completo da un error de timeout
        """
        index = 1
        end_index = index + self.increment - 1
        last_line = []
        rows = gsheet_list[0]
        for r in rows:
            last_line.append('')

        letter = chr(ord('A') - 1 + len(rows))

        while True:
            update_range = '{sheet}!A{line}:{column}'.format(sheet=sheet, line=index, column=letter)
            sub_list = gsheet_list[index - 1:end_index]
            if not sub_list:
                break

            sub_list.append(last_line)
            body = {
                'values': sub_list
            }
            self.services['sheet'].spreadsheets().values().update(
                spreadsheetId=self.file_id,
                range=update_range,
                valueInputOption='RAW',
                body=body
            ).execute()
            print("Added rows to the sheet {} from {} to {}".format(sheet, index, len(sub_list) - 1),)

            index = end_index + 1
            end_index = index + self.increment - 1
            # time.sleep(0.5)

    def create_data_sheet(self):
        gsheet_list = self.database.coronavirus_data_list()

        self.upload_gsheet_data(
            gsheet_list=gsheet_list,
            sheet='coronavirus'
        )
        return

    def create_countries_sheet(self):
        gsheet_countries = self.database.coronavirus_geography_list()
        self.upload_gsheet_data(
            gsheet_list=gsheet_countries,
            sheet='geography'
        )
        return

    def set_filename(self, filename):
        self.filename = filename
        self.get_gdrive_file_id()


    def __init__(self):
        self.gsheet_service()
        self.get_gdrive_file_id()
