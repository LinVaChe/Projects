from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

DATABASE_URL = "postgresql://postgres:Algov16lu@localhost:5432/laba_3"
#ПАРОЛЬ ТЕПЕРЬ БЕЗ СКОБОЧКИ

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)

Base = declarative_base()
