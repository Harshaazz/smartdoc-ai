from app.services.semantic_search_service import (
    generate_embedding
)

embedding = generate_embedding(
    "Invoice Number Amount GST"
)

print("Embedding Length:", len(embedding))