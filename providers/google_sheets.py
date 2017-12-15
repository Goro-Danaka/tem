import os
import sys
import gspread

from oauth2client.service_account import ServiceAccountCredentials


class GoogleSheets:
    scope = ['https://spreadsheets.google.com/feeds']
    key_filename = 'google-key.json'

    def __init__(self):
        config_dir_path = os.path.join(sys.path[0], 'config')
        key_file_path = os.path.normpath(os.path.join(config_dir_path, self.key_filename))
        creds = ServiceAccountCredentials.from_json_keyfile_name(key_file_path, self.scope)
        client = gspread.authorize(creds)
        sheet = client.open("Test").sheet1
        list_of_hashes = sheet.get_all_records()
