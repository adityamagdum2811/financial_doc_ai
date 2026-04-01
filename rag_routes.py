from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app import models, schemas
from app.deps import get_current_user, require_role
from app.rag import index_document, remove_document, semantic_search, get_document_context

router = APIRouter(prefix="/rag", tags=["RAG"])


@router.post("/index-document")
def index_doc(
    document_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(require_role(["Admin", "Financial Analyst", "Auditor"]))
):
    doc = db.query(models.Document).filter(models.Document.id == document_id).first()
    if not doc:
        raise HTTPException(status_code=404, detail="Document not found")

    if not doc.extracted_text:
        raise HTTPException(status_code=400, detail="No extracted text available")

    chunk_count = index_document(doc.id, doc.extracted_text)
    return {"message": "Document indexed successfully", "chunks_created": chunk_count}


@router.delete("/remove-document/{document_id}")
def remove_doc_embedding(
    document_id: int,
    current_user=Depends(require_role(["Admin"]))
):
    removed_ids = remove_document(document_id)
    return {"message": "Embeddings removed", "removed_chunks": removed_ids}


@router.post("/search")
def rag_search(
    payload: schemas.RagSearchRequest,
    current_user=Depends(get_current_user)
):
    results = semantic_search(payload.query)
    return {"query": payload.query, "results": results}


@router.get("/context/{document_id}")
def rag_context(
    document_id: int,
    current_user=Depends(get_current_user)
):
    context = get_document_context(document_id)
    return {"document_id": document_id, "context_chunks": context}