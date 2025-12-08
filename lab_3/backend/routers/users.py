from fastapi import APIRouter, Depends, HTTPException, status, Header
from sqlalchemy.orm import Session
from ..database import SessionLocal  # путь может быть ../database
from backend.models import User            # убедись, что модель в backend/models.py
from passlib.context import CryptContext
from backend.schemas import *
import secrets


router = APIRouter(prefix="/api/users", tags=["users"])
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def get_db(): #получает сессию БД
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/register", response_model=UserOut, status_code=status.HTTP_201_CREATED)
def register_user(payload: UserCreate, db: Session = Depends(get_db)):
    if db.query(User).filter(User.email == payload.email).first():
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Email already registered")

    hashed = pwd_context.hash(payload.password)
    new_user = User(
        username=payload.username,
        email=payload.email,
        password_hash=hashed,
        sex=payload.sex,
        paytype=payload.paytype,
        country=payload.country,
        infoabout=payload.infoabout
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user


# --- LOG IN ---
@router.post("/login")
def login(payload: UserLogin, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == payload.email).first()

    if not user:
        raise HTTPException(status_code=400, detail="Неверный email или пароль")

    if not pwd_context.verify(payload.password, user.password_hash):
        raise HTTPException(status_code=400, detail="Неверный email или пароль")

    # Генерируем токен
    token = secrets.token_hex(32)
    user.access_token = token
    db.commit()

    return {"message": "Успешная авторизация", "access_token": token}


# --- LOGOUT ---
@router.post("/logout")
def logout(token: str, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.access_token == token).first()

    if not user:
        raise HTTPException(status_code=401, detail="Неверный токен")

    user.access_token = None
    db.commit()

    return {"message": "Вы вышли из аккаунта"}


# --- GET CURRENT USER ---
@router.get("/me")
def get_me(token: str = Header(None), db: Session = Depends(get_db)):
    if not token:
        raise HTTPException(status_code=401, detail="Нет токена")

    user = db.query(User).filter(User.access_token == token).first()

    if not user:
        raise HTTPException(status_code=401, detail="Неверный токен")

    return {
        "username": user.username,
        "email": user.email,
        "sex": user.sex,
        "country": user.country,
        "paytype": user.paytype,
        "infoabout": user.infoabout,
    }
