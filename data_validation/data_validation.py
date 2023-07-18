from pydantic import BaseModel, field_validator, Field
import logging

logging.basicConfig(format='%(asctime)s %(message)s')
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

class Orders(BaseModel):
    order_id: int = Field(..., gt=0)
    customer_id: int = Field(..., gt=0)
    product_id: int = Field(..., gt=0)
    quantity: int
    price: float
    order_date: str

    class Config:
        validate_assignment = True

    @field_validator('quantity')
    def validate_quantity(cls, value):
        if value < 0:
            raise ValueError('Quantity cannot be negative')
        return value

    @field_validator('price')
    def validate_price(cls, value):
        if value < 0:
            raise ValueError('Price cannot be negative')
        return value


class Users(BaseModel):
    id: int = Field(..., gt=0)
    name: str
    username: str
    email: str
    address_geo_lat: str
    address_geo_lng: str

    class Config:
        validate_assignment = True


def validate_users_data(data):
    users = [Users(**row) for _, row in data.iterrows()]
    logger.info("validation successful for users data")


def validate_orders_data(data):
    order = [Orders(**row) for _, row in data.iterrows()]
    logger.info("validation successful for orders data")

