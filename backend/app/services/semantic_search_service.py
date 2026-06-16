from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np

model = SentenceTransformer(
    "all-MiniLM-L6-v2"
)


def generate_embedding(text):

    embedding = model.encode(
        text
    )

    return embedding.tolist()


def calculate_similarity(
    query_embedding,
    document_embedding
):

    similarity = cosine_similarity(
        [query_embedding],
        [document_embedding]
    )

    return float(similarity[0][0])