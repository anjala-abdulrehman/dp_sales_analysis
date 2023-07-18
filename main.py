from data_aggregation.sales_data_aggregations import generate_and_write_aggregations
from data_extraction.api_to_dl import raw_data_to_dl
from data_extraction.dl_table_creations import raw_table_creation_sqllite
from data_load.dw_table_creations import aggregate_table_creation_sqllite

"""
The main function
 1. Creates raw table if it doesn't exists in the db
 2. Ingests data from various sources, and is written to dl
 3. Performs aggregations and the transformations are written to dw
"""
if __name__ == '__main__':
    raw_table_creation_sqllite()
    aggregate_table_creation_sqllite()
    raw_data = raw_data_to_dl()
    generate_and_write_aggregations(raw_data)
