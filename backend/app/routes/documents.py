from fastapi import (
    APIRouter,
    UploadFile,
    File,
    Depends,
    Query
)

from app.utils.auth_middleware import verify_token
from app.services.classifier_service import (
    classify_document
)
from app.services.semantic_search_service import (
    generate_embedding
)
from app.services.ocr_service import (
    extract_text_from_image,
    extract_text_from_pdf
)
from app.services.document_service import (
    save_document_metadata,
    get_user_documents,
    search_documents,
    get_documents_by_type,
    get_dashboard_stats,
    semantic_search_documents
)

import os
import shutil


router = APIRouter(
    prefix="/documents",
    tags=["Documents"]
)

UPLOAD_FOLDER = "app/uploads"
@router.get("/search")
async def search_document(
    q: str,
    user=Depends(verify_token)
):
    results = await search_documents(
        user["email"],
        q
    )

    return results
@router.get("/semantic-search")
async def semantic_search(
    q: str,
    user=Depends(verify_token)
):

    results = await semantic_search_documents(
        user["email"],
        q
    )

    return results


@router.get("/")
async def get_documents(
    user=Depends(verify_token)
):
    documents = await get_user_documents(
        user["email"]
    )

    return documents

@router.post("/upload")
async def upload_document(
    file: UploadFile = File(...),
    user=Depends(verify_token)
):

    os.makedirs(
        UPLOAD_FOLDER,
        exist_ok=True
    )

    file_path = os.path.join(
        UPLOAD_FOLDER,
        file.filename
    )

    with open(
        file_path,
        "wb"
    ) as buffer:

        shutil.copyfileobj(
            file.file,
            buffer
        )

    ocr_text = ""

    try:

        if file.filename.lower().endswith(
            (".png", ".jpg", ".jpeg")
        ):

            ocr_text = extract_text_from_image(
                file_path
            )

        elif file.filename.lower().endswith(
            ".pdf"
        ):

            ocr_text = extract_text_from_pdf(
                file_path
            )

        print("=" * 50)
        print("OCR RESULT:")
        print(repr(ocr_text[:500]))
        print("=" * 50)

    except Exception as e:

        print("OCR Error:", e)

    document_type = classify_document(
        ocr_text
    )
    

    print("DOCUMENT TYPE:", document_type)
    embedding = generate_embedding(
    ocr_text
    )

    document_id = await save_document_metadata(
        filename=file.filename,
        filepath=file_path,
        uploaded_by=user["email"],
        extracted_text=ocr_text,
        document_type=document_type,
        embedding=embedding
    )

    return {
        "message": "File uploaded successfully",
        "document_id": document_id,
        "filename": file.filename,
        "ocr_text": ocr_text,
        "document_type": document_type
    }
@router.get("/type/{document_type}")
async def get_documents_type(
    document_type: str,
    user=Depends(verify_token)
):

    documents = await get_documents_by_type(
        user["email"],
        document_type
    )

    return documents

@router.get("/dashboard/stats")
async def dashboard_stats(
    user=Depends(verify_token)
):

    stats = await get_dashboard_stats(
        user["email"]
    )

    return stats

@router.get("/type/{document_type}")
async def get_documents_type(
    document_type: str,
    user=Depends(verify_token)
):

    documents = await get_documents_by_type(
        user["email"],
        document_type
    )

    return documents

