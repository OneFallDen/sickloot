from fastapi import routing, Depends
from sqlalchemy.orm import Session

from sql.db import get_db
from models.schemas import User
from controllers.user_controller import get_current_user
from controllers.inventory_controller import get_inventory


router = routing.APIRouter()


@router.get('/inventory/user', tags=['inventory'])
async def get_user_inventory(user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    return get_inventory(user.id, db)
