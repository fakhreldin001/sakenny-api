"""
Embedding service for Sakenny
Uses a free local model - no API key needed
"""

from sentence_transformers import SentenceTransformer

# Load the model once when the app starts
# all-MiniLM-L6-v2 is small, fast, and free
model = SentenceTransformer("all-MiniLM-L6-v2")


def generate_embedding(text: str) -> list[float]:
    """
    Takes text and returns a 384-dimension vector.
    Similar texts will have similar vectors.
    """
    embedding = model.encode(text)
    return embedding.tolist()


def build_property_text(property_data: dict) -> str:
    """
    Combines property fields into one string for embedding.
    This way the vector captures the full picture of the property.
    """
    parts = []

    if property_data.get("title"):
        parts.append(property_data["title"])
    if property_data.get("location"):
        parts.append(f"located in {property_data['location']}")
    if property_data.get("price"):
        parts.append(f"price {property_data['price']} EGP")
    if property_data.get("bedrooms"):
        parts.append(f"{property_data['bedrooms']} bedrooms")
    if property_data.get("property_type"):
        parts.append(f"type {property_data['property_type']}")
    if property_data.get("description"):
        parts.append(property_data["description"])

    return ". ".join(parts)
