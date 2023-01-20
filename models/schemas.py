from datetime import datetime
from pydantic import BaseModel, EmailStr
from enum import Enum


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    user_id: int | None = None


class User(BaseModel):
    id: int
    login: str
    password: str
    email: EmailStr
    opened_cases: int
    level: int
    steam_acc_url: str
    role: int
    balance: int


class UserAuth(BaseModel):
    login: str
    password: str


class UserReg(UserAuth):
    email: EmailStr
    repeat_password: str


class UserInDB(User):
    hashed_password: str


class windrow_history(BaseModel):
    user_id: int
    win_rep: int
    date: datetime


class drop_history(BaseModel):
    user_id: int
    case_id: int
    item_id: int
    date_of_drop: datetime


class inventory(BaseModel):
    user_id: int
    item_id: int


class rarityEnum(str, Enum):
    immortal = "Immortal"
    ancient = "Ancient"
    arcana = "Arcana"
    season = "Season"
    legendary = "Legendary"
    mythical = "Mythical"
    uncommon = "Uncommon"
    common = "Common"
    rare = "Rare"


class item(BaseModel):
    id: int
    name: str
    character: str
    rarity: rarityEnum
    type: str
    price: int


class case_items(BaseModel):
    case_id: int
    item_id: int


class case(BaseModel):
    id: int
    name: str
    price: int


class set_items(BaseModel):
    set_id: int
    item_id: int


class sett(BaseModel):
    id: int
    character: str
    name: str
    price: int
