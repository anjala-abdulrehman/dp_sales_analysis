db_name = 'sales_data_aggregations'


# Create a table in the database
ttl_sales_amt_per_cust_tbl_query = '''
CREATE TABLE IF NOT EXISTS ttl_sales_amt_per_cust (
    customer_id INTEGER PRIMARY KEY,
    order_date TEXT,
    ttl_sales_amt_per_cust FLOAT
);
'''

avg_order_qty_per_prod_tbl_query = '''
CREATE TABLE IF NOT EXISTS avg_order_qty_per_prod (
    product_id INTEGER PRIMARY KEY,
    order_date TEXT,
    avg_order_qty_per_prod FLOAT
);
'''

sales_summary_for_year_tbl_query = '''
CREATE TABLE IF NOT EXISTS sales_summary_for_year (
    order_year INTEGER PRIMARY KEY,
    sales_summary_for_year_tbl_query FLOAT
);
'''

sales_summary_for_quarter_tbl_query = '''
CREATE TABLE IF NOT EXISTS sales_summary_for_quarter (
    order_quarter INTEGER PRIMARY KEY,
    sales_summary_for_quarter_tbl_query INT
);
'''

sales_summary_for_month_tbl_query = '''
CREATE TABLE IF NOT EXISTS sales_summary_for_month (
    order_month INTEGER PRIMARY KEY,
    sales_summary_for_month_tbl_query INT
);
'''


sales_summary_for_week_tbl_query = '''
CREATE TABLE IF NOT EXISTS sales_summary_for_week (
    order_week INTEGER PRIMARY KEY,
    sales_summary_for_week_tbl_query INT
);
'''

most_reordered_products_tbl_query = '''
CREATE TABLE IF NOT EXISTS most_reordered_products (
    product_id INTEGER PRIMARY KEY,
    most_reordered_products INT
);
'''

avg_days_to_reorder_tbl_query = '''
CREATE TABLE IF NOT EXISTS avg_days_to_reorder (
    product_id INTEGER PRIMARY KEY,
    date_diffs FLOAT
);
'''

avg_sales_amt_per_weather_condition_tbl_query = '''
CREATE TABLE IF NOT EXISTS avg_sales_amt_per_weather_condition (
    weather_conditions TEXT PRIMARY KEY,
    order_year TEXT, 
    avg_sales_amt_per_weather_condition FLOAT
);
'''

ttl_sales_qty_per_weather_condition_tbl_query = '''
CREATE TABLE IF NOT EXISTS ttl_sales_qty_per_weather_condition (
    weather_conditions TEXT PRIMARY KEY,
    order_year TEXT, 
    ttl_sales_qty_per_weather_condition FLOAT
);
'''

best_sold_product_per_weather_conditions_tbl_query = '''
CREATE TABLE IF NOT EXISTS best_sold_product_per_weather_conditions (
    weather_conditions TEXT PRIMARY KEY,
    order_year TEXT, 
    best_sold_product_per_weather_conditions FLOAT
);
'''

tbl_create_queries = {
    'ttl_sales_amt_per_cust_tbl_query': ttl_sales_amt_per_cust_tbl_query,
    'avg_order_qty_per_prod_tbl_query': avg_order_qty_per_prod_tbl_query,
    'sales_summary_for_year_tbl_query': sales_summary_for_year_tbl_query,
    'sales_summary_for_quarter_tbl_query': sales_summary_for_quarter_tbl_query,
    'sales_summary_for_month_tbl_query': sales_summary_for_month_tbl_query,
    'sales_summary_for_week_tbl_query' : sales_summary_for_week_tbl_query,
    'most_reordered_products_tbl_query': most_reordered_products_tbl_query,
    'avg_days_to_reorder_tbl_query': avg_days_to_reorder_tbl_query,
    'avg_sales_amt_per_weather_condition_tbl_query': avg_sales_amt_per_weather_condition_tbl_query,
    'ttl_sales_qty_per_weather_condition_tbl_query': ttl_sales_qty_per_weather_condition_tbl_query,
    'best_sold_product_per_weather_conditions_tbl_query': best_sold_product_per_weather_conditions_tbl_query
}
