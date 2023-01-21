from sqlalchemy.orm import Session

from sql.crud import get_case_by_id, get_case_items
from models.schemas import User


def get_case(case_id: int, db: Session):
    return get_case_by_id(case_id, db)


def get_case_with_items(case_id: int, db: Session):
    case = get_case_by_id(case_id, db)
    items = get_case_items(case_id, db)
    return {
        'item': items
    }
