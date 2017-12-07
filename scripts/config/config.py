caravancampingsales = {
    'connection_string': 'pq://postgres:qwerty@195.69.187.40:5432/',
    'db_name': 'caravancampingsales',
    'table_name': 'goods_3',
    'original_name_table': 'good_columns_3',
    'csv_name': 'caravancampingsales-%s.csv',
    'basic_columns': [],
    'unique_column': '',
    'result_path': 'results',
    'csv_header_order': ['id', 'Category', 'SubCategory', 'Make', 'Model', 'Year', 'Engine Horsepower', 'Fuel Type', 'Sleeping Capacity', 'Seating Capacity', 'Suspension', 'Transmission', 'Brakes', 'Length', 'GVM', 'Tare', 'Tow Ball Weight', 'ATM', 'Size'],
    'proxy_enabled': False
}

pitchup = {
    'connection_string': 'pq://postgres:qwerty@195.69.187.40:5432/',
    'db_name': 'pitchup',
    'table_name': 'parks_test1',
    'original_name_table': 'park_columns_test1',
    'csv_name': 'pitchup-%s.csv',
    'basic_columns': ['name', 'latitude', 'longitude', 'grade', 'street_address', 'locality', 'region',
                      'country_name',
                      'postal_code'],
    'unique_column': 'name',
    'result_path': 'results',
    'csv_header_order': [],
    'proxy_enabled': False
}

defaults = {
    'caravancampingsales': caravancampingsales,
    'pitchup':  pitchup
}