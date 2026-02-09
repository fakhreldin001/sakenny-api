from sqlalchemy import Column, Integer, String, Float, DateTime
from datetime import datetime
from src.db.database import Base
from pgvector.sqlalchemy import Vector

class Property(Base):
    __tablename__ = "properties"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    description = Column(String)
    price = Column(Float, nullable=False)
    location = Column(String, nullable=False)
    bedrooms = Column(Integer)
    bathrooms = Column(Integer)
    area = Column(Float)  # in square meters
    property_type = Column(String)  # apartment, villa, studio, etc.
    created_at = Column(DateTime, default=datetime.utcnow)
    embedding = Column(Vector(384), nullable=True)