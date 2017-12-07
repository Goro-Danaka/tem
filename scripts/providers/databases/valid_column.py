import base64

from scripts.providers.logging_provider import LoggingProvider


class ValidColumn:

    def __init__(self):
        self.logging_provider = LoggingProvider()

    def encode_column(self, column_name):
        try:
            if column_name == 'name':
                return column_name
            result = []
            for char in column_name:
                if char.isspace():
                    result.append('_')
                elif char.isalpha() or char.isdigit():
                    result.append(char)
            return ''.join(result).lower()
        except Exception as ex:
            self.logging_provider.warning('Can\'t encode column: %s; Exception: \n%s' % (column_name, ex))
            return column_name

    def decode_column(self, column_name):
        try:
            if column_name == 'name':
                return column_name
            decoded = base64.decodestring(bytes(column_name, 'utf-8'))
            return decoded
        except Exception as ex:
            self.logging_provider.warning('Can\'t decode column: %s; Exception: \n%s' % (column_name, ex))
            return column_name

    def encode_object_info(self, object_info):
        encoded_object_info = {}
        for column in object_info:
            encoded_column = self.encode_column(column)
            encoded_object_info[encoded_column] = object_info[column]
        return encoded_object_info

    def decode_object_info(self, object_info):
        decoded_object_info = {}
        for column in object_info:
            decoded_column = self.encode_column(column)
            decoded_object_info[decoded_column] = object_info[column]
        return decoded_object_info

    def decode_columns(self, columns):
        decoded_columns = []
        for column in columns:
            decoded_columns.append(self.decode_column(column))
        return decoded_columns


