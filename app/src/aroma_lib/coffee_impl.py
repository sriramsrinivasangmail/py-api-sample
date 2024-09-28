from typing import List

from generated.dependencies import *
from generated.models import *


def list_coffees() -> List[Coffee]:
    """
    List all coffees
    """

    return []


def create_coffee(body: Coffee) -> None:
    """
    Add a new coffee
    """

    return body


def update_coffee(body: Coffee) -> None:
    """
    Update a coffee
    """

    return body


def delete_coffee(coffee_name: str) -> None:
    """
    Delete a coffee by name
    """

    pass


def get_coffee_by_name(name: str) -> Coffee:
    """
    Get a coffee by name
    """

    dummy_data={"name": "dummy", "description": "dummy desc", "quantity": 7.5, "origin": "India", "packaging_data": "beans", "price": 13.99 }
    dummy = Coffee(**dummy_data)

    return dummy
