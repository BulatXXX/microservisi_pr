from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
import os
#DATABASE_URL = "postgresql://postgres:1@localhost:5432/staff_management"
DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://postgres:1@localhost:5433/staff_management")
engine = create_engine(DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

def init_db():
    Base.metadata.create_all(bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()