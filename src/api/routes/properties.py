from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import text
from src.db.database import get_db
from src.db.models.property import Property
from src.api.schemas import PropertyCreate, PropertyResponse
from src.ai.embeddings import generate_embedding, build_property_text

router = APIRouter(prefix="/properties", tags=["Properties"])


@router.post("/", response_model=PropertyResponse)
def create_property(property_data: PropertyCreate, db: Session = Depends(get_db)):
    # Convert property data to a dictionary
    data = property_data.model_dump()
    
    # Generate embedding from property details
    text = build_property_text(data)
    data["embedding"] = generate_embedding(text)
    
    new_property = Property(**data)
    db.add(new_property)
    db.commit()
    db.refresh(new_property)
    return new_property


@router.get("/", response_model=list[PropertyResponse])
def get_all_properties(
    db: Session = Depends(get_db),
    location: str | None = None,
    min_price: float | None = None,
    max_price: float | None = None,
    bedrooms: int | None = None,
    property_type: str | None = None
):
    query = db.query(Property)

    if location:
        query = query.filter(Property.location.ilike(f"%{location}%"))
    if min_price:
        query = query.filter(Property.price >= min_price)
    if max_price:
        query = query.filter(Property.price <= max_price)
    if bedrooms:
        query = query.filter(Property.bedrooms == bedrooms)
    if property_type:
        query = query.filter(Property.property_type == property_type)

    return query.all()


@router.get("/{property_id}", response_model=PropertyResponse)
def get_property(property_id: int, db: Session = Depends(get_db)):
    property = db.query(Property).filter(Property.id == property_id).first()
    if not property:
        raise HTTPException(status_code=404, detail="Property not found")
    return property


@router.put("/{property_id}", response_model=PropertyResponse)
def update_property(property_id: int, property_data: PropertyCreate, db: Session = Depends(get_db)):
    property = db.query(Property).filter(Property.id == property_id).first()
    if not property:
        raise HTTPException(status_code=404, detail="Property not found")

    data = property_data.model_dump()
    
    # Regenerate embedding when property is updated
    text = build_property_text(data)
    data["embedding"] = generate_embedding(text)

    for key, value in data.items():
        setattr(property, key, value)

    db.commit()
    db.refresh(property)
    return property


@router.delete("/{property_id}")
def delete_property(property_id: int, db: Session = Depends(get_db)):
    property = db.query(Property).filter(Property.id == property_id).first()
    if not property:
        raise HTTPException(status_code=404, detail="Property not found")

    db.delete(property)
    db.commit()
    return {"message": "Property deleted"}


@router.get("/search/semantic")
def semantic_search(query: str, limit: int = 5, db: Session = Depends(get_db)):
    """
    Search properties by meaning, not exact words.
    Example: "quiet place near downtown for students" 
    will find relevant properties even if they don't use those exact words.
    """
    # Convert the search query into numbers (embedding)
    query_embedding = generate_embedding(query)
    
    # Find properties whose embeddings are closest to the query
    # <=> is pgvector's distance operator - smaller = more similar
    results = db.execute(
        text("""
            SELECT id, title, description, price, location, bedrooms, 
                   bathrooms, area, property_type,
                   embedding <=> :query_embedding AS distance
            FROM properties
            WHERE embedding IS NOT NULL
            ORDER BY distance
            LIMIT :limit
        """),
        {"query_embedding": "[" + ",".join(str(float(x)) for x in query_embedding) + "]", "limit": limit}
    ).fetchall()
    
    return [
        {
            "id": r.id,
            "title": r.title,
            "description": r.description,
            "price": r.price,
            "location": r.location,
            "bedrooms": r.bedrooms,
            "bathrooms": r.bathrooms,
            "area": r.area,
            "property_type": r.property_type,
            "similarity_score": round(1 - r.distance, 4)
        }
        for r in results
    ]

@router.get("/{property_id}/similar")
def find_similar_properties(property_id: int, limit: int = 3, db: Session = Depends(get_db)):
    """
    Find properties similar to a given property.
    Uses the property's embedding to find the closest matches.
    """
    # Get the original property
    property = db.query(Property).filter(Property.id == property_id).first()
    if not property:
        raise HTTPException(status_code=404, detail="Property not found")
    if property.embedding is None:
        raise HTTPException(status_code=400, detail="Property has no embedding")

    results = db.execute(
        text("""
            SELECT id, title, description, price, location, bedrooms,
                   bathrooms, area, property_type,
                   embedding <=> :query_embedding AS distance
            FROM properties
            WHERE embedding IS NOT NULL AND id != :property_id
            ORDER BY distance
            LIMIT :limit
        """),
        {
            "query_embedding": "[" + ",".join(str(float(x)) for x in property.embedding) + "]",
            "property_id": property_id,
            "limit": limit
        }
    ).fetchall()

    return [
        {
            "id": r.id,
            "title": r.title,
            "description": r.description,
            "price": r.price,
            "location": r.location,
            "bedrooms": r.bedrooms,
            "bathrooms": r.bathrooms,
            "area": r.area,
            "property_type": r.property_type,
            "similarity_score": round(1 - r.distance, 4)
        }
        for r in results
    ]