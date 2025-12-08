from fastapi import FastAPI
from .routers import users, reviews,  products
from fastapi.middleware.cors import CORSMiddleware
from backend.init_base import create_test_data
from backend.database import SessionLocal

app = FastAPI()

origins = [
    "http://127.0.0.1:8000",  
    "http://localhost:8000",
   
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins, 
    allow_credentials=True,
    allow_methods=["*"],        
    allow_headers=["*"],       
) 

""" db = SessionLocal()
create_test_data(db)
db.close() """

app.include_router(users.router)
app.include_router(products.router)
app.include_router(reviews.router)  


