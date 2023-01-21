from fastapi import routing, Depends
from sqlalchemy.orm import Session

from sql.db import get_db
from models.schemas import User
from controllers.case_controller import get_case, get_case_with_items
from controllers.user_controller import get_current_user


router = routing.APIRouter()


@router.get('/case/info', tags=['case'])
async def get_case_info(case_id: int, db: Session = Depends(get_db)):
    return get_case(case_id, db)


@router.get('/case/items/info', tags=['case'])
async def get_case_and_items_info(case_id: int, db: Session = Depends(get_db)):
    return get_case_with_items(case_id, db)


@router.post('/case/open', tags=['case'])
async def open_case(case_id, db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    return 1