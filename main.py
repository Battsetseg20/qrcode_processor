from fastapi import FastAPI
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import DeclarativeMeta, declarative_base
from sqlalchemy.orm import sessionmaker

app = FastAPI()

DATABASE_URL = "postgresql://localhost/qrcode_processor_db"
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base: DeclarativeMeta = declarative_base()

@app.get("/")
def read_root():
    return {"message": "Hello, world!"}
