from fastapi import FastAPI

app = FastAPI(
    title="Sakenny API",
    description="Property listing API for the Egyptian real estate market",
    version="0.1.0"
)

@app.get("/")
def root():
    return {"status": "Sakenny API is alive"}

@app.get("/health")
def health_check():
    return {"status": "healthy"}