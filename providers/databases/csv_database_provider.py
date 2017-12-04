import csv
import os
import sys
import codecs



from providers.logging_provider import LoggingProvider
from config.config import defaults


class CsvDatabaseProvider:

    def __init__(self):
        self.logging_provider = LoggingProvider()
        #self.csv_name = defaults[config_name]['csv_name']
        #self.basic_columns = defaults[config_name]['basic_columns']

    def insert(self, objects_info, config):
        try:
            result_path = os.path.join(sys.path[0], 'result')
            result_path = os.path.join(result_path, defaults[config]['result_dir_template'])
            if not os.path.exists(result_path):
                os.makedirs(result_path)
            file_path = os.path.join(result_path, 'data.csv')
            with open(file_path, 'w', encoding='utf-8', newline='') as csvfile:
                fieldnames = defaults[config]['fields']
                writable_header = self.get_writable_header(fieldnames)
                writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
                writer.writerow(writable_header)
                for object_info in objects_info:
                    if object_info:
                        writer.writerow(object_info)
        except Exception as ex:
            #self.logging_provider.critical('CsvDatabaseProvider; Error in method insert:'
            #                               ' - object - \n%s\nException: \n%s' % (objects_info, ex))
            return None

    def utf_8_encoder(self, unicode_csv_data):
        for line in unicode_csv_data:
            yield line.encode('utf-8')

    def generate_csv_header(self, static_header, objects):
        try:
            fieldnames = []
            fieldnames.extend(static_header)
            for object in objects:
                for key in object:
                    if key not in fieldnames:
                        fieldnames.append(key)
            return fieldnames
        except Exception as ex:
            self.logging_provider.critical('Error in method generate_csv_header: static_header - '
                                           '\n%s\nobjects - %s\n Exception: \n%s' % (static_header, objects, ex))
            return None

    def get_writable_header(self, fieldnames):
        try:
            writeable_header = {}
            for fieldname in fieldnames:
                writeable_header[fieldname] = fieldname
            return writeable_header
        except Exception as ex:
            self.logging_provider.critical('Error in method get_writable_header: fieldnames - '
                                           '\n%s\nException: \n%s' % (fieldnames, ex))
            return None



