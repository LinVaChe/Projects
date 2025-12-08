from pydantic import BaseModel, EmailStr
from typing import Optional

class UserCreate(BaseModel):
    username: str
    email: EmailStr
    password: str
    sex: str
    paytype: str
    country: str
    infoabout: Optional[str] = None

class UserOut(BaseModel):
    userid: int
    username: str
    email: EmailStr
    class Config:
        orm_mode = True

class LoginIn(BaseModel):
    email: EmailStr
    password: str

class UserUpdate(BaseModel):
    username: Optional[str] = None
    country: Optional[str] = None
    infoabout: Optional[str] = None

class UserLogin(BaseModel):
    email: str
    password: str

class UserOut(BaseModel):
    userid: int
    username: str
    email: str
    sex: str
    paytype: str
    country: str
    infoabout: str | None

    class Config:
        from_attributes = True

class ReviewCreate(BaseModel):
    text: str

class ReviewOut(BaseModel):
    id: int
    user_id: int
    text: str
    username: str

    class Config:
        orm_mode = True

class ProductBase(BaseModel):
    productname: str
    category: str
    short_description: Optional[str]
    description: Optional[str]
    price: float
    image: Optional[str]
    available: bool


class ProductOut(ProductBase):
    productid: int

    class Config:
        orm_mode = True