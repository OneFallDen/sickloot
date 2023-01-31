from fastapi import routing, Depends
from sqlalchemy.orm import Session

from sql.db import get_db
from models.schemas import User
from controllers.user_controller import get_current_user
from controllers.inventory_controller import get_inventory, sell_item_from_user_inventory


router = routing.APIRouter()


@router.get('/inventory/user', tags=['inventory'])
async def get_user_inventory(user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    return get_inventory(user.id, db)


@router.post('/inventory/sell', tags=['inventory'])
async def sell_item_from_inventory(item_id: int, user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    return sell_item_from_user_inventory(item_id, user.id, db)
