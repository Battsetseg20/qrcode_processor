# database.py
import os

from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

load_dotenv()

DATABASE_URL = os.environ["DATABASE_URL"]

"""
Database setup
"""

try:
    engine = create_engine(DATABASE_URL, echo=True)
except Exception as e:
    print("Unable to access postgresql database", repr(e))

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
        db.commit()
    except Exception as e:
        db.rollback()
        print(f"Error in #get_db: {e}")
    finally:
        db.close()
