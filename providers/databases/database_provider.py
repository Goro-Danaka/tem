from scripts.providers.databases.db_type import DBType
from scripts.providers.logging_provider import LoggingProvider
from scripts.providers.databases.csv_database_provider import CsvDatabaseProvider
from scripts.providers.databases.postgresql_database_provider import PostgreSQLDatabaseProvider


class DatabaseProvider:

    db_provider = None

    def __init__(self, config_name, db_type=DBType.POSTGRE_SQL):
        self.logging_provider = LoggingProvider()
        self.init_db_provider(config_name=config_name, db_type=db_type)

    def init_db_provider(self, config_name, db_type):
        try:
            if db_type == DBType.CSV:
                self.db_provider = CsvDatabaseProvider(config_name)
            else:
                self.db_provider = PostgreSQLDatabaseProvider(config_name)
        except Exception as ex:
            self.logging_provider.critical('Error in init_db_provider: db_type - %s\n Exception: \n%s' % (db_type, ex))

    def insert(self, objects_info):
        try:
            if not self.db_provider:
                self.logging_provider.warning('Can\'t insert while databases provider not initialized')
                return
            self.db_provider.insert(objects_info)
        except Exception as ex:
            self.logging_provider.critical('DatabaseProvider; Error in method insert: - parks_info - \n%s\nException: \n%s' % (objects_info, ex))
            return None

    def export_to_csv(self):
        self.db_provider.export_to_csv()


