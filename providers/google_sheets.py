import os
import sys
import gspread

from config.config import defaults
from gspread.exceptions import SpreadsheetNotFound
from gspread.exceptions import WorksheetNotFound
from providers.logging_provider import LoggingProvider
from oauth2client.service_account import ServiceAccountCredentials


class GoogleSheets:
    scope = ['https://spreadsheets.google.com/feeds']
    key_filename = 'google-key.json'
    sheet = None
    worksheet = None

    def __init__(self):
        self.lp = LoggingProvider()
        config_dir_path = os.path.join(sys.path[0], 'config')
        self.key_file_path = os.path.normpath(os.path.join(config_dir_path, self.key_filename))
        self.credentials = ServiceAccountCredentials.from_json_keyfile_name(self.key_file_path, self.scope)
        self.client = gspread.authorize(self.credentials)

    def set_worksheet(self, name):
        try:
            is_success = True
            if not self.sheet:
                sheet_name = defaults['sheet_name']
                self.sheet = self.client.open(sheet_name)
            is_worksheet_exist = self._is_worksheet_exist(name)
            if not is_worksheet_exist:
                self.worksheet = self.sheet.add_worksheet(title=name, rows=100000, cols=8)
            else:
                self.worksheet = self.sheet.worksheet(title=name)
        except SpreadsheetNotFound as SheetException:
            self.lp.critical('Can\'t open main sheet. Exception: \n"%s"' % SheetException)
            is_success = False
        except Exception as ex:
            self.lp.critical('Exception was thrown. \n"%s"' % ex)
            is_success = False
        finally:
            return is_success

    def update_cell(self, next_id, product_info):
        self.worksheet.update_cell(next_id, 1, product_info['Title'])
        self.worksheet.update_cell(next_id, 2, product_info['Category'])
        self.worksheet.update_cell(next_id, 3, product_info['Url'])
        self.worksheet.update_cell(next_id, 4, product_info['Description'])
        self.worksheet.update_cell(next_id, 5, product_info['Price'])
        self.worksheet.update_cell(next_id, 6, product_info['Sale price'])
        self.worksheet.update_cell(next_id, 7, product_info['Currency'])
        self.worksheet.update_cell(next_id, 8, GoogleSheets.get_images_string(product_info['Images']))

    def update(self, product_info):
        try:
            cell_list = self.worksheet.findall(product_info['Url'])
            next_id = len(self.worksheet.get_all_values()) + 1 if not len(cell_list) else cell_list[0].row
            self.update_cell(next_id, product_info)
        except Exception as ex:
            pass

    @staticmethod
    def get_images_string(images):
        result = ''
        for image in images:
            result += '%s;' % image
        return result

    def _is_worksheet_exist(self, name):
        try:
            is_exist = True
            worksheet = self.sheet.worksheet(name)
        except WorksheetNotFound as WorkSheetException:
            is_exist = False
            self.lp.warning('Worksheet not exist. It will be created.' % WorkSheetException)
        finally:
            return is_exist
