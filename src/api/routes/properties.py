from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from src.db.database import get_db
from src.db.models.property import Property
from src.api.schemas import PropertyCreate, PropertyResponse

router = APIRouter(prefix="/properties", tags=["Properties"])

@router.post("/", response_model=PropertyResponse)
def create_property(property_data: PropertyCreate, db: Session = Depends(get_db)):
    new_property = Property(**property_data.model_dump())
    db.add(new_property)
    db.commit()
    db.refresh(new_property)
    return new_property

@router.get("/", response_model=list[PropertyResponse])
def get_all_properties(db: Session = Depends(get_db)):
    return db.query(Property).all()

@router.get("/{property_id}", response_model=PropertyResponse)
def get_property(property_id: int, db: Session = Depends(get_db)):
    property = db.query(Property).filter(Property.id == property_id).first()
    if not property:
        raise HTTPException(status_code=404, detail="Property not found")
    return property