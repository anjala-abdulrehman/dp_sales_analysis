from datetime import datetime as dt
import pandas as pd
from data_load.config import db_name
from data_load.data_aggregations_to_dw import data_to_dw as aggregations_to_dw
import logging

logging.basicConfig(format='%(asctime)s %(message)s')
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)


# Calculate total sales amount per customer.
def ttl_sales_amt_per_cust(sorted_data: pd.DataFrame) -> None:
    """
    :param sorted_data: sorted master data
    Output is writen to data warehouse
    """
    sorted_data['ttl_sales_amt_per_cust'] = sorted_data.groupby(['customer_id', 'order_date'])['price'].cumsum()
    sorted_data = sorted_data[["customer_id", "order_date", "ttl_sales_amt_per_cust"]]
    aggregations_to_dw(sorted_data, db_name, 'ttl_sales_amt_per_cust')


# Determine the average order quantity per product.
def avg_order_qty_per_prod(sorted_data: pd.DataFrame) -> None:
    """
    :param sorted_data: sorted master data
    Output is writen to data warehouse
    """
    running_sum = sorted_data.groupby(['product_id', 'order_date'])['quantity'].cumsum()
    cumulative_count = sorted_data.groupby(['product_id', 'order_date']).cumcount() + 1
    sorted_data['avg_order_qty_per_prod'] = running_sum / cumulative_count
    sorted_data = sorted_data[["product_id", "order_date", "avg_order_qty_per_prod"]]
    aggregations_to_dw(sorted_data, db_name, 'avg_order_qty_per_prod')


# Identify the top-selling products for customers. (for ?)

def get_top_selling_stats(sorted_data: pd.DataFrame) -> None:
    """
    :param sorted_data: sorted master data
    Output is writen to data warehouse
    """
    sorted_data['top_selling_prod_for_cust'] = sorted_data.groupby(['customer_id', 'order_date'])[
        'product_id'].cumcount()

    # Analyze sales trends over time (e.g., monthly or quarterly sales).
    sorted_data['order_year'] = sorted_data['order_date'].apply(lambda x: (dt.strptime(x, '%Y-%m-%d')).year)
    sorted_data['order_quarter'] = sorted_data['order_date'].apply(
        lambda x: (dt.strptime(x, '%Y-%m-%d').month - 1) // 3 + 1)
    sorted_data['order_month'] = sorted_data['order_date'].apply(lambda x: (dt.strptime(x, '%Y-%m-%d')).month)
    sorted_data['order_week'] = sorted_data['order_date'].apply(
        lambda x: (dt.strptime(x, '%Y-%m-%d')).isocalendar().week)

    sales_summary_for_year = pd.DataFrame(sorted_data.groupby('order_year')['order_id'].count().reset_index())
    sales_summary_for_year.rename(columns={'order_id': 'sales_summary_for_year'}, inplace=True)
    sales_summary_for_qtr = pd.DataFrame(sorted_data.groupby(['order_year', 'order_quarter'])['order_id'].count().reset_index())
    sales_summary_for_qtr.rename(columns={'order_id': 'sales_summary_for_qtr'}, inplace=True)
    sales_summary_for_mnth = pd.DataFrame(sorted_data.groupby(['order_year', 'order_month'])['order_id'].count().reset_index())
    sales_summary_for_mnth.rename(columns={'order_id': 'sales_summary_for_mnth'}, inplace=True)
    sales_summary_for_cw = pd.DataFrame(sorted_data.groupby(['order_year', 'order_week'])['order_id'].count().reset_index())
    sales_summary_for_cw.rename(columns={'order_id': 'sales_summary_for_cw'}, inplace=True)

    aggregations_to_dw(sales_summary_for_year, db_name, 'sales_summary_for_year')
    aggregations_to_dw(sales_summary_for_qtr, db_name, 'sales_summary_for_qtr')
    aggregations_to_dw(sales_summary_for_mnth, db_name, 'sales_summary_for_mnth')
    aggregations_to_dw(sales_summary_for_cw, db_name, 'sales_summary_for_cw')


# 1. reordered products Aggregations

def reordered_products_stats(master_data: pd.DataFrame) -> None:
    """
    :param master_data: master data
    Output is writen to data warehouse
    """
    orders_data = master_data.sort_values(['customer_id', 'order_id'])
    orders_data['reordered_flag'] = orders_data.groupby(['customer_id', 'product_id'])[
        'order_id'].shift().notnull().astype(
        int)
    most_reordered_products = orders_data.groupby('product_id')['reordered_flag'].sum().reset_index()[:3]

    # 2. time to re-order
    orders_data['reordered_date'] = orders_data.groupby(['customer_id', 'product_id'])['order_date'].shift()
    orders_data['date_diffs'] = [
        abs((dt.strptime(str(j), '%Y-%m-%d').date()) - dt.strptime(str(i), '%Y-%m-%d').date()).days if (
                i and j and str(i) != 'nan' and str(j) != 'nan') else None for i, j in
        zip(orders_data['order_date'], orders_data['reordered_date'])]
    avg_days_to_reorder = orders_data.groupby('product_id')['date_diffs'].mean().reset_index()

    aggregations_to_dw(most_reordered_products, db_name, 'most_reordered_products')
    aggregations_to_dw(avg_days_to_reorder, db_name, 'avg_days_to_reorder')


# Include weather data in the analysis (e.g., average sales amount per weather condition).
def sales_analysis_for_weather_condition(sorted_data: pd.DataFrame) -> None:
    """
    :param sorted_data: master data
    Output is writen to data warehouse
    """
    sorted_data['order_year'] = sorted_data['order_date'].apply(lambda x: (dt.strptime(x, '%Y-%m-%d')).year)
    avg_sales_amt_per_weather_condition = sorted_data.groupby(['weather_conditions', 'order_year'])['price'].sum().reset_index()
    ttl_sales_qty_per_weather_condition = sorted_data.groupby(['weather_conditions', 'order_year'])['quantity'].sum().reset_index()
    ttl_product_sold_per_weather_condition = sorted_data.groupby(['weather_conditions', 'order_year', 'product_id'])[
        'quantity'].sum()
    best_sold_product_per_weather_conditions = ttl_product_sold_per_weather_condition.groupby(
        ['weather_conditions', 'order_year']).nlargest(3).reset_index(level=[0, 1], drop=True)
    ttl_product_sold_per_weather_condition = ttl_product_sold_per_weather_condition.reset_index()
    aggregations_to_dw(avg_sales_amt_per_weather_condition, db_name, 'avg_sales_amt_per_weather_condition')
    aggregations_to_dw(ttl_sales_qty_per_weather_condition, db_name, 'ttl_sales_qty_per_weather_condition')
    aggregations_to_dw(best_sold_product_per_weather_conditions, db_name, 'best_sold_product_per_weather_conditions')
    aggregations_to_dw(ttl_product_sold_per_weather_condition, db_name, 'ttl_product_sold_per_weather_condition')


def generate_and_write_aggregations(master_data: pd.DataFrame):
    """
    :param master_data: master data
    Output is writen to data warehouse
    """
    sorted_df = master_data.sort_values('order_date')

    aggregations = [
        (sales_analysis_for_weather_condition, [sorted_df]),
        (ttl_sales_amt_per_cust, [sorted_df]),
        (avg_order_qty_per_prod, [sorted_df]),
        (get_top_selling_stats, [sorted_df]),
        (reordered_products_stats, [master_data]),
    ]

    for agg_func_name, data in aggregations:
        logger.info(f"Processing Aggregation: {agg_func_name.__name__}")
        agg_func_name(*data)
        logger.info(f"Processing Aggregation: {agg_func_name.__name__} Complete")
