import pandas as pd
import requests
import logging
from datetime import datetime
from data_extraction.config import urls_and_path_config, users_tbl_config, api_key, db_config
from concurrent.futures import ThreadPoolExecutor
from tenacity import retry, stop_after_attempt, wait_fixed
from data_validation.data_validation import validate_users_data, validate_orders_data
from data_load.data_aggregations_to_dw import data_to_dw

executor = ThreadPoolExecutor(max_workers=4)

logging.basicConfig(format='%(asctime)s %(message)s')
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
db_name = db_config['raw_db_name']


def load_orders_data(path=urls_and_path_config['sales_data_path']) -> pd.DataFrame:
    """
    :param path: sales data path
    :return: orders data:
    """
    orders_data = pd.read_csv(path)
    validate_orders_data(orders_data)
    data_to_dw(orders_data, db_name, 'orders')
    logger.info(
        f"Orders Data Loaded to Datalake at {datetime.now()}, and has {orders_data.shape[0]} rows and {orders_data.shape[1]} columns")

    return orders_data


@retry(stop=stop_after_attempt(3), wait=wait_fixed(1))
def _query_users_api(url: str):
    """
    :param url: users api url
    :return: users data as a row
    """
    response = requests.get(url)
    response.raise_for_status()
    return pd.json_normalize(response.json())


def query_users_api(url: str = urls_and_path_config['users_url']) -> pd.DataFrame:
    """
    :param url: url to query users
    :return: users data
    """
    try:
        users_data = _query_users_api(url)
        users_data = users_data[users_tbl_config['cols']]
        users_data.rename(columns=lambda x: x.replace('.', '_'), inplace=True)
        validate_users_data(users_data)
        data_to_dw(users_data, db_name, 'users')

        logger.info(f"Users Data Loaded to Datalake at {datetime.now()}, and has {users_data.shape[0]} rows and {users_data.shape[1]} columns")
        return users_data
    except requests.exceptions.RequestException as e:
        logger.info(f"Error making API request {(str(e))}")


def query_weather_api(master_data: pd.DataFrame) -> pd.DataFrame:
    """
    :param master_data: combined data
    :return: master data with weather data added
    """
    master_data[['temperature', 'feels_like', 'weather_conditions']] = list(
        executor.map(apply, master_data['address_geo_lat'], master_data['address_geo_lng']))

    return master_data


@retry(stop=stop_after_attempt(3), wait=wait_fixed(10))
def _query_weather_api(lat, lon) -> tuple:
    weather_url = urls_and_path_config['weather_url']

    url = f'{weather_url}?lat={lat}&lon={lon}&appid={api_key}'
    response = requests.get(url)
    response_data = response.json()
    return (
        response_data['main']['temp'],
        response_data['main']['feels_like'],
        response_data['weather'][0]['main']
            )


def apply(lat, lon):
    try:
        weather_data = _query_weather_api(lat, lon)
        return weather_data
    except requests.exceptions.RequestException as e:
        logger.info("Error querying weather API:", str(e))
    except Exception as e:
        logger.info("Max retry limit reached:", str(e))


def raw_data_to_dl():
    """
    Runs data from the sources and merged and then loaded to datalake
    :return: All data from sources
    """
    logger.info("Starting execution: Fetching Sales Data")
    sales_data = load_orders_data()

    logger.info(f"Fetching Sales Data: Complete.. Starting execution: Fetching Users Data")

    users_data = query_users_api()
    logger.info(f"Fetching Users Data: Complete")
    sales_and_users_data = sales_data.merge(users_data, how='left', left_on='customer_id', right_on='id')
    logger.info("Starting execution: Fetching Weather Data")
    master_data = query_weather_api(sales_and_users_data)
    data_to_dw(master_data, db_name, 'master_data')
    logger.info(
        f"Master Data Loaded to Datalake at {datetime.now()}, and has {master_data.shape[0]} rows and {master_data.shape[1]} columns")

    logger.info(
        f"Fetching Weather Data: Completed at {datetime.now()}, and the master data has {master_data.shape[0]} rows and {master_data.shape[1]} columns")

    return master_data
