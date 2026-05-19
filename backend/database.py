from sqlalchemy import create_engine, Column, Integer, String, Float, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from datetime import datetime

DATABASE_URL = "sqlite:///./property_analysis.db"

engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

class PropertyListing(Base):
    __tablename__ = "property_listings"

    id = Column(Integer, primary_key=True, index=True)
    address = Column(String, index=True)
    latitude = Column(Float)
    longitude = Column(Float)
    asking_price = Column(Float)
    area = Column(Float)
    age = Column(Integer)
    building_type = Column(String)
    floor = Column(Integer)
    total_floors = Column(Integer)
    parking = Column(String)
    layout = Column(String)
    created_at = Column(DateTime, default=datetime.utcnow)

class TransactionRecord(Base):
    __tablename__ = "transaction_records"

    id = Column(Integer, primary_key=True, index=True)
    address = Column(String, index=True)
    latitude = Column(Float)
    longitude = Column(Float)
    price = Column(Float)
    area = Column(Float)
    age = Column(Integer)
    building_type = Column(String)
    floor = Column(Integer)
    transaction_date = Column(String)
    district = Column(String)

Base.metadata.create_all(bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
