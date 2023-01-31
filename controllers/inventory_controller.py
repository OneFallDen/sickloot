from sqlalchemy.orm import Session
from fastapi import HTTPException

from sql.crud import get_inventory_items, delete_item_from_inventory, get_item_by_id, update_balance


def get_inventory(user_id: int, db: Session):
    return get_inventory_items(user_id, db)


def sell_item_from_user_inventory(item_id: int, user_id: int, db: Session):
    delete_item_from_inventory(item_id, user_id, db)
    item = get_item_by_id(item_id, db)
    update_balance(item.price, user_id, db)
    return HTTPException(status_code=201, detail='Item deleted successfully')
