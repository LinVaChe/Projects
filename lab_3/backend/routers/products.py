from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from ..database import SessionLocal  # путь может быть ../database
from ..models import Product, ProductProperty
from ..schemas import ProductBase, ProductOut

router = APIRouter(prefix="/products", tags=["Products"])

def get_db(): #получает сессию БД
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Получить все товары категории
@router.get("/category/{category}", response_model=list[ProductOut])
def get_products_by_category(category: str, db: Session = Depends(get_db)):
    return db.query(Product).filter(Product.category == category).all()


# Получить полный товар по ID
@router.get("/{product_id}")
def get_product(product_id: int, db: Session = Depends(get_db)):
    product = db.query(Product).filter(Product.productid == product_id).first()

    if not product:
        raise HTTPException(status_code=404, detail="Товар не найден")

    properties = (
        db.query(ProductProperty)
        .filter(ProductProperty.productid == product_id)
        .all()
    )

    return {
        "product": product,
        "properties": properties
    }

@router.get("/", response_model=list[ProductBase])
def get_all_products(db: Session = Depends(get_db)):
    return db.query(Product).all()
