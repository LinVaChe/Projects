from fastapi import APIRouter, Depends, HTTPException, Header
from sqlalchemy.orm import Session
from ..database import SessionLocal  # путь может быть ../database
from ..models import Review, User
from ..schemas import ReviewCreate, ReviewOut
import random

router = APIRouter(prefix="/api/reviews", tags=["Reviews"])

def get_db(): #получает сессию БД
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/", response_model=dict)
def create_review(
    review: ReviewCreate,
    authorization: str = Header(None),
    db: Session = Depends(get_db)
):
    if not authorization:
        raise HTTPException(status_code=401, detail="Нет токена")

    token = authorization.replace("Bearer ", "")

    user = db.query(User).filter(User.access_token == token).first()
    if not user:
        raise HTTPException(status_code=401, detail="Неверный токен")

    new_review = Review(user_id=user.userid, review_text=review.text)
    db.add(new_review)
    db.commit()
    db.refresh(new_review)

    return {"status": "ok", "review_id": new_review.review_id}


@router.get("/random", response_model=list[ReviewOut])
def get_random_reviews(db: Session = Depends(get_db)):
    reviews = db.query(Review).join(User).all()

    # берём максимум 3 случайных
    selected = random.sample(reviews, min(3, len(reviews)))

    return [
        ReviewOut(
            id=r.review_id,
            user_id=r.user_id,
            text=r.review_text,
            username=r.user.username
        )
        for r in selected
    ]