import sqlite3
import logging
from data_extraction.config import raw_tbl_queries_config

logging.basicConfig(format='%(asctime)s %(message)s')
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)


def raw_table_creation_sqllite():
    """
    Creates raw sources data tables
    """
    data_conn = sqlite3.connect('raw_source_data.db')
    data_cursor = data_conn.cursor()

    for name, table_queries in raw_tbl_queries_config.items():
        logger.info(f"executing {name}")
        data_cursor.execute(table_queries)

    data_conn.commit()
    data_conn.close()










