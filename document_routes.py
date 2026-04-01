import os
from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, Form
from sqlalchemy.orm import Session
from app.database import get_db
from app import models, schemas
from app.deps import get_current_user, require_role
from app.utils import save_upload_file, extract_text
from app.config import settings

router = APIRouter(prefix="/documents", tags=["Documents"])


@router.post("/upload")
def upload_document(
    title: str = Form(...),
    company_name: str = Form(...),
    document_type: str = Form(...),
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
    current_user=Depends(require_role(["Admin", "Financial Analyst"]))
):
    file_path = os.path.join(settings.upload_dir, file.filename)
    save_upload_file(file, file_path)
    extracted = extract_text(file_path)

    doc = models.Document(
        title=title,
        company_name=company_name,
        document_type=document_type,
        file_path=file_path,
        extracted_text=extracted,
        uploaded_by=current_user.id
    )
    db.add(doc)
    db.commit()
    db.refresh(doc)

    return {"message": "Document uploaded", "document_id": doc.id}


@router.get("/", response_model=list[schemas.DocumentResponse])
def get_all_documents(
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    docs = db.query(models.Document).all()
    return docs


@router.get("/{document_id}", response_model=schemas.DocumentResponse)
def get_document(
    document_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    doc = db.query(models.Document).filter(models.Document.id == document_id).first()
    if not doc:
        raise HTTPException(status_code=404, detail="Document not found")
    return doc


@router.delete("/{document_id}")
def delete_document(
    document_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(require_role(["Admin"]))
):
    doc = db.query(models.Document).filter(models.Document.id == document_id).first()
    if not doc:
        raise HTTPException(status_code=404, detail="Document not found")

    if os.path.exists(doc.file_path):
        os.remove(doc.file_path)

    db.delete(doc)
    db.commit()

    return {"message": "Document deleted successfully"}


@router.get("/search/")
def search_documents(
    title: str | None = None,
    company_name: str | None = None,
    document_type: str | None = None,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    query = db.query(models.Document)

    if title:
        query = query.filter(models.Document.title.ilike(f"%{title}%"))
    if company_name:
        query = query.filter(models.Document.company_name.ilike(f"%{company_name}%"))
    if document_type:
        query = query.filter(models.Document.document_type.ilike(f"%{document_type}%"))

    return query.all()