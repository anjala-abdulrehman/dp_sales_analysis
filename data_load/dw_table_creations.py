import sqlite3

from data_load.config import tbl_create_queries


def aggregate_table_creation_sqllite():
    """
    Creates raw sources data tables
    """
    stats_data_conn = sqlite3.connect('sales_data_aggregations.db')
    stats_data_cursor = stats_data_conn.cursor()

    for _, table_queries in tbl_create_queries.items():
        stats_data_cursor.execute(table_queries)

    stats_data_conn.commit()
    stats_data_conn.close()
