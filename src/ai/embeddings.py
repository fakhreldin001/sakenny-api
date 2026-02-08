"""
Embedding service for Sakenny
Generates vector embeddings for property descriptions using OpenAI
"""

import os
from openai import OpenAI

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def generate_embedding(text: str) -> list[float]:
    """
    Takes a text description and returns a 1536-dimension vector.
    This vector captures the semantic meaning of the text,
    so similar descriptions will have similar vectors.
    """
    response = client.embeddings.create(
        model="text-embedding-3-small",
        input=text
    )
    return response.data[0].embedding


def build_property_text(property_data: dict) -> str:
    """
    Combines all property fields into a single string for embedding.
    
    Why: Instead of embedding just the title, we combine location, price,
    bedrooms, type, etc. so the vector captures the full picture.
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