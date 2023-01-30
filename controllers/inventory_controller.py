from sqlalchemy.orm import Session
from fastapi import HTTPException

from sql.crud import get_inventory_items


def get_inventory(user_id: int, db: Session):
    return get_inventory_items(user_id, db)
