import gspread
from config.config import defaults
from oauth2client.service_account import ServiceAccountCredentials


class DatabaseProvider:
    def __init__(self):
        #scope = ['https://spreadsheets.google.com/feeds']
        #api_key_file_path = defaults['api_key_file_path']
        #credentials = ServiceAccountCredentials.from_json_keyfile_name(api_key_file_path, scope)
        #gc = gspread.authorize(credentials)
        #wks = gc.open("Where is the money Lebowski?").sheet1
        #wks.update_acell('B2', "it's down there somewhere, let me take another look.")
        #cell_list = wks.range('A1:B7')
        pass