import pandas as pd
import sqlite3


def data_to_dw(data: pd.DataFrame, db_name: str, tbl_name: str) -> None:
    """
    :param data: df to be written to dw
    :param db_name: db that holds the data
    Writes the data to dw
    """
    connection = sqlite3.connect(db_name)
    data.to_sql(tbl_name, connection, if_exists='replace', index=False)
    connection.close()
