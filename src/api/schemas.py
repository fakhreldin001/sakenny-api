from pydantic import BaseModel
from datetime import datetime

class PropertyCreate(BaseModel):
    title: str
    description: str | None = None
    price: float
    location: str
    bedrooms: int | None = None
    bathrooms: int | None = None
    area: float | None = None
    property_type: str | None = None

class PropertyResponse(PropertyCreate):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True