import postgresql
import os
import sys
import csv
import datetime

from scripts.providers.databases.valid_column import ValidColumn
from scripts.providers.logging_provider import LoggingProvider
from scripts.config.config import defaults


class PostgreSQLDatabaseProvider:

    csv_header = None
    column_names = None
    real_csv_header = None

    def __init__(self, config_name):
        self.valid_column = ValidColumn()
        self.logging_provider = LoggingProvider()
        self.unique_code = defaults[config_name]['unique_column']
        self.db_name = defaults[config_name]['db_name']
        self.connection_string = defaults[config_name]['connection_string'] + self.db_name
        self.table_name = defaults[config_name]['table_name']
        self.csv_name = defaults[config_name]['csv_name']
        self.basic_columns = defaults[config_name]['basic_columns']
        self.original_name_table = defaults[config_name]['original_name_table']
        self.result_path = defaults[config_name]['result_path']
        self.csv_header_order = defaults[config_name]['csv_header_order']
        with postgresql.open(self.connection_string) as self.db:
            self.create_tables()

    def is_values_table_initialized(self):
        if not len(self.basic_columns) and self.is_column_exist('id', self.table_name):
            return True
        elif not len(self.basic_columns) and not self.is_column_exist('id', self.table_name):
            return False
        for column_name in self.basic_columns:
            if not self.is_column_exist(column_name, self.table_name):
                return False
        return True

    def is_original_names_db_initialized(self):
        if not self.is_column_exist('name', self.original_name_table):
            return False
        if not self.is_column_exist('original_name', self.original_name_table):
            return False
        return True

    def is_column_exist(self, column_name, table_name):
        try:
            exist_script = "SELECT column_name " \
                           "FROM information_schema.columns " \
                           "WHERE table_name='%s' and " \
                           "column_name='%s';" % (table_name, column_name)
            result = self.db.query(exist_script)
            return bool(len(result))
        except Exception as ex:
            self.logging_provider.critical('Excepted on is_column_exist method. Exception: \n%s' % ex)

    def add_column(self, column_name):
        try:
            is_column_exist = self.is_column_exist(column_name, self.table_name)
            if not is_column_exist:
                column_type = "VARCHAR(255)" if column_name in self.basic_columns else "VARCHAR(255)"
                add_script = self.db.prepare("ALTER TABLE %s ADD %s %s;" % (self.table_name, column_name, column_type))
                result = add_script()
                if result and result.__sizeof__() > 1:
                    self.logging_provider.info("Added column: %s; result: %s" % (column_name, result))
        except Exception as ex:
            self.logging_provider.critical('Excepted on add_column method. Exception: \n%s' % ex)

    def get_entry_id_by_name(self, entry_name, value):
        try:
            result = self.db.query("SELECT id FROM %s WHERE %s='%s'" % (self.table_name, entry_name, value))
            if result and result.__sizeof__() > 0:
                self.logging_provider.info("Entry %s has id: %s" % (entry_name, result[0]))
                return result[0]
        except Exception as ex:
            self.logging_provider.critical('Excepted on get_entry_id_by_name. Exception: \n%s' % ex)

    def get_original_column_name(self, column_name):
        try:
            if column_name == 'id':
                return 'id'
            result = self.db.query("SELECT original_name FROM %s WHERE name='%s'" % (self.original_name_table, column_name))
            if result and result.__sizeof__() > 0:
                return result[0][0]
            else:
                return column_name
        except Exception as ex:
            self.logging_provider.critical('Excepted on get_original_column_name. name: %s; Exception: \n%s' % (column_name, ex))

    def create_tables(self):
        is_values_table_initialized = self.is_values_table_initialized()
        is_original_names_table_initialized = self.is_original_names_db_initialized()
        if not is_values_table_initialized:
            self.create_values_table()
        if not is_original_names_table_initialized:
            self.create_original_names_table()

    def create_original_names_table(self):
        try:
            create_table_script = "CREATE TABLE %s (id SERIAL PRIMARY KEY," \
                                  " name VARCHAR(256)," \
                                  " original_name VARCHAR(256)) "
            self.db.execute(create_table_script[:-1] % self.original_name_table)
        except Exception as ex:
            self.logging_provider.critical('Excepted on create_tables. Exception: \n%s' % ex)

    def create_values_table(self):
        try:
            create_table_script = "CREATE TABLE %s (id SERIAL PRIMARY KEY"
            script_end = ')'
            for column in self.basic_columns:
                create_table_script += ", %s VARCHAR(256)" % column
            self.db.execute((create_table_script if len(self.basic_columns) else create_table_script) % self.table_name + script_end)
        except Exception as ex:
            self.logging_provider.critical('Excepted on create_tables. Exception: \n%s' % ex)

    def insert_script_from_object_info(self, object_info):
        insert_script_columns = "INSERT INTO %s (" % self.table_name
        insert_script_values = " VALUES ("
        for key in object_info:
            insert_script_columns = insert_script_columns + " " + key + ","
            insert_script_values = insert_script_values + " " + "'" + self.validate_value(str(object_info[key])) + "',"
        insert_script_columns = insert_script_columns[:-1] + ")"
        insert_script_values = insert_script_values[:-1] + ")"
        insert_script = insert_script_columns + insert_script_values
        return insert_script

    def insert_script_from_column_names(self, column_name, original_column_name):
        insert_script = "INSERT INTO %s (name, original_name) VALUES ('%s', '%s')" % (self.original_name_table, column_name, self.validate_value(original_column_name))
        return insert_script

    def validate_value(self, value):
        result = []
        for char in value:
            if char.isspace():
                result.append(' ')
            elif char.isalpha() or char.isdigit():
                result.append(char)
        return ''.join(result)

    def insert(self, object_info):
        with postgresql.open(self.connection_string) as self.db:
            object_info_columns = list(object_info.keys())
            i = 0
            while i < len(object_info_columns):
                column = self.valid_column.encode_column(object_info_columns[i])
                is_column_exist = self.is_column_exist(column, self.table_name)
                if not is_column_exist:
                    self.add_column(column)
                    insert_original_name_script = self.insert_script_from_column_names(column, object_info_columns[i])
                    ins_original_name = self.db.prepare(insert_original_name_script)
                    ins_original_name()
                i += 1
            encoded_object_info = self.valid_column.encode_object_info(object_info)
            if self.unique_code in encoded_object_info:
                result = self.get_entry_id_by_name(self.unique_code, self.validate_value(encoded_object_info[self.unique_code]))
                if result and result.__sizeof__() > 0:
                    self.logging_provider.critical('Entry %s is alredy exist:' % encoded_object_info[self.unique_code])
                    return

            insert_script = self.insert_script_from_object_info(encoded_object_info)
            ins = self.db.prepare(insert_script)
            ins()

    def export_to_csv(self):
        with postgresql.open(self.connection_string) as self.db:
            self.db.execute("DECLARE object_cursor CURSOR WITH HOLD FOR "
                   "SELECT * FROM %s" % self.table_name)

            cursor = self.db.cursor_from_id("object_cursor")
            is_first_entry = True
            objects_info = []
            values = cursor.read()
            original_column_names = {}
            for value in values:
                if value:
                    if is_first_entry:
                        self.csv_header = {}
                        self.real_csv_header = []
                        self.column_names = cursor.column_names
                        for column_name in self.column_names:
                            original_column_name = self.get_original_column_name(column_name)
                            original_column_names[column_name] = original_column_name
                            self.csv_header[original_column_name] = original_column_name
                            self.real_csv_header.append(original_column_name)
                        objects_info.append(self.csv_header)
                        is_first_entry = False
                    i = 0
                    object_info = {}
                    while i < len(self.column_names):
                        object_info[original_column_names[self.column_names[i]]] = str(value[i])
                        i += 1
                    objects_info.append(object_info)
            self.write_to_csv(objects_info)
            cursor.close()

    def write_to_csv(self, objects_info):
        try:
            result_path = os.path.join(sys.path[0], self.result_path)
            if not os.path.exists(result_path):
                os.makedirs(result_path)
            file_name = os.path.join(result_path, self.csv_name % datetime.datetime.now().strftime("%Y-%m-%d-%H-%M-%S"))
            ordered_csv_header = self.order_csv_header(self.real_csv_header)
            with open(file_name, 'w') as csvfile:
                writer = csv.DictWriter(csvfile, fieldnames=ordered_csv_header)
                for park_info in objects_info:
                    writer.writerow(park_info)
        except Exception as ex:
            self.logging_provider.critical(
                'Error in method write_to_csv: - objects_info - \n%s\nException: \n%s' % (
                    objects_info, ex))
            return None

    def order_csv_header(self, csv_header):
        if not self.csv_header_order or not len(self.csv_header_order):
            return csv_header
        ordered_csv_header = []
        for column in self.csv_header_order:
            if column in csv_header:
                ordered_csv_header.append(column)
        for column in self.csv_header:
            if column not in ordered_csv_header:
                ordered_csv_header.append(column)
        return ordered_csv_header



