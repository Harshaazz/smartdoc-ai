from app.database.mongodb import db
from datetime import datetime

async def save_document_metadata(
    filename: str,
    filepath: str,
    uploaded_by: str,
    extracted_text: str = "",
    document_type: str = "Other",
    embedding=None
):

    document = {
        "filename": filename,
        "filepath": filepath,
        "uploaded_by": uploaded_by,
        "uploaded_at": datetime.utcnow(),
        "status": "processed",
        "document_type": document_type,
        "extracted_text": extracted_text,
        "embedding": embedding,
    }

    result = await db.documents.insert_one(document)

    return str(result.inserted_id)
async def get_user_documents(email: str):

    documents = []

    cursor = db.documents.find(
        {
            "uploaded_by": email
        }
    )

    async for doc in cursor:

        documents.append({
    "id": str(doc["_id"]),
    "filename": doc["filename"],
    "document_type": doc.get("document_type", "Other"),
    "status": doc["status"],
    "uploaded_at": doc["uploaded_at"],
    "ocr_preview": doc.get("extracted_text", "")[:100]
})

    return documents
async def search_documents(
    email: str,
    query: str
):

    documents = []

    cursor = db.documents.find(
        {
            "uploaded_by": email,
            "extracted_text": {
                "$regex": query,
                "$options": "i"
            }
        }
    )

    async for doc in cursor:

        documents.append({
            "id": str(doc["_id"]),
            "filename": doc["filename"],
            "status": doc["status"],
            "ocr_preview": doc.get(
                "extracted_text",
                ""
            )[:200]
        })

    return documents

async def get_documents_by_type(
    email: str,
    document_type: str
):

    documents = []

    cursor = db.documents.find(
        {
            "uploaded_by": email,
            "document_type": document_type
        }
    )

    async for doc in cursor:

        documents.append({
            "id": str(doc["_id"]),
            "filename": doc["filename"],
            "document_type": doc.get(
                "document_type",
                "Other"
            ),
            "status": doc["status"],
            "uploaded_at": doc["uploaded_at"]
        })

    return documents
async def get_dashboard_stats(email: str):

    total_documents = await db.documents.count_documents(
        {
            "uploaded_by": email
        }
    )

    invoices = await db.documents.count_documents(
        {
            "uploaded_by": email,
            "document_type": "Invoice"
        }
    )

    contracts = await db.documents.count_documents(
        {
            "uploaded_by": email,
            "document_type": "Contract"
        }
    )

    resumes = await db.documents.count_documents(
        {
            "uploaded_by": email,
            "document_type": "Resume"
        }
    )

    others = await db.documents.count_documents(
    {
        "uploaded_by": email,
        "$or": [
            {"document_type": "Other"},
            {"document_type": {"$exists": False}}
        ]
    }
)

    return {
        "total_documents": total_documents,
        "invoices": invoices,
        "contracts": contracts,
        "resumes": resumes,
        "others": others
    }
from app.services.semantic_search_service import (
    generate_embedding,
    calculate_similarity
)


async def semantic_search_documents(
    email: str,
    query: str
):

    query_embedding = generate_embedding(
        query
    )

    documents = []

    cursor = db.documents.find(
        {
            "uploaded_by": email,
            "embedding": {
                "$exists": True
            }
        }
    )

    async for doc in cursor:

        similarity = calculate_similarity(
            query_embedding,
            doc["embedding"]
        )

        documents.append({
            "filename": doc["filename"],
            "document_type": doc.get(
                "document_type",
                "Other"
            ),
            "similarity": similarity
        })

    documents.sort(
        key=lambda x: x["similarity"],
        reverse=True
    )

    return documents[:5]
