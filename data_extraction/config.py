urls_and_path_config = {
    'users_url': 'https://jsonplaceholder.typicode.com/users',
    'weather_url': 'https://api.openweathermap.org/data/2.5/weather',
    'sales_data_path': 'data/raw/sales/sales_data.csv'
}

users_tbl_config = {
    'cols': ['id', 'name', 'username', 'email', 'address.geo.lat',  'address.geo.lng']
}

# Create a table in the database
create_orders_table_query = '''
CREATE TABLE IF NOT EXISTS orders (
    order_id INTEGER PRIMARY KEY,
    customer_id INTEGER,
    product_id INTEGER,
    quantity INTEGER,
    price FLOAT,
    order_date TEXT
);
'''

create_users_table_query = '''
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY,
    name TEXT,
    username TEXT,
    email TEXT,
    address_geo_lat TEXT,
    address_geo_lng TEXT
);
'''

create_master_table_query = '''
CREATE TABLE IF NOT EXISTS master_data (
    order_id INTEGER,
    customer_id INTEGER,
    product_id INTEGER,
    quantity INTEGER,
    price REAL,
    order_date TEXT,
    id INTEGER,
    name TEXT,
    username TEXT,
    email TEXT,
    address_geo_lat REAL,
    address_geo_lng REAL,
    temperature REAL,
    feels_like REAL,
    weather_conditions TEXT
);
'''


raw_tbl_queries_config = {
    'orders': create_orders_table_query,
    'users': create_users_table_query,
    'master_data': create_master_table_query,
}

db_config = {
    'raw_db_name': 'raw_source_data.db'
}

api_key = 'd00187d387aa9617ed13b01d9577f3d0'


