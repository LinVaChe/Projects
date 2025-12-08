from sqlalchemy import Column, Integer, String, Boolean, Numeric, Text, ForeignKey
from sqlalchemy.orm import relationship
from .database import Base

class User(Base):
    __tablename__ = "users"
    userid = Column(Integer, primary_key=True, index=True)
    username = Column(String(20), nullable=False)
    email = Column(String(50), nullable=False, unique=True)
    sex = Column(String(10), nullable=False)
    paytype = Column(String(10), nullable=False)
    country = Column(String(15), nullable=False)
    infoabout = Column(String(255))
    password_hash = Column(String(255), nullable=False)
    access_token = Column(String(255), nullable = False)

class Review(Base):
    __tablename__ = "reviews"

    review_id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.userid"))
    review_text = Column(Text)

    user = relationship("User")

class Product(Base):
    __tablename__ = "products"

    productid = Column(Integer, primary_key=True)
    productname = Column(String(100), nullable=False)
    category = Column(String(50), nullable=False)
    short_description = Column(String(255))
    description = Column(Text)
    price = Column(Numeric(10, 2), nullable=False)
    image = Column(Text)
    available = Column(Boolean, default=True)

    properties = relationship("ProductProperty", back_populates="product", cascade="all, delete")


class ProductProperty(Base):
    __tablename__ = "product_properties"

    propertyid = Column(Integer, primary_key=True)
    productid = Column(Integer, ForeignKey("products.productid"))
    property_name = Column(String(100), nullable=False)
    property_value = Column(String(255), nullable=False)

    product = relationship("Product", back_populates="properties")
