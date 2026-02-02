from fastapi import FastAPI

from src.db.database import engine, Base
from src.db.models.property import Property
from src.api.routes.properties import router as properties_router

app = FastAPI(
    title="Sakenny API",
    description="Property listing API for the Egyptian real estate market",
    version="0.1.0"
)

Base.metadata.create_all(bind=engine)

app.include_router(properties_router)

@app.get("/")
def root():
    return {"status": "Sakenny API is alive"}

@app.get("/health")
def health_check():
    return {"status": "healthy"}