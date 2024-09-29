from typing import List

from generated.dependencies import *
from generated.models import *

def get_order_by_id(order_id: str) -> Order:
    """
    Get an order by order_id

    """

    dummy_data={"order_id": "0000-1234", "deliver_date": "2024-09-30", "customer_name": "Homer J. Simpson",  "order_items": None, "sale_price": 93.99, "status": "pending" }
    dummy = Order(**dummy_data)

    return dummy
