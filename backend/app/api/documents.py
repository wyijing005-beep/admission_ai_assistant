import os
import io
from pathlib import Path
from fastapi import APIRouter, UploadFile, File, Depends
from sqlalchemy.orm import Session

from app.models.schemas import DocumentUploadResponse
from app.models.user import User
from app.rag import embedding_store, chunker
from app.core.config import settings
from app.core.database import get_db
from app.api.auth import get_current_user

router = APIRouter()


def _parse_pdf(file_bytes: bytes) -> str:
    from pypdf import PdfReader
    reader = PdfReader(io.BytesIO(file_bytes))
    parts = []
    for page in reader.pages:
        text = page.extract_text()
        if text:
            parts.append(text)
    return "\n".join(parts)


@router.post("/documents/upload", response_model=DocumentUploadResponse)
def upload_document(
    file: UploadFile = File(...),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    content = file.read()

    filename_lower = file.filename.lower()
    if filename_lower.endswith(".pdf"):
        try:
            text = _parse_pdf(content)
        except Exception:
            return DocumentUploadResponse(
                filename=file.filename,
                chunks=0,
                status="pdf_parse_error",
            )
        if not text.strip():
            return DocumentUploadResponse(
                filename=file.filename,
                chunks=0,
                status="pdf_empty",
            )
    else:
        for encoding in ["utf-8", "gbk", "gb2312"]:
            try:
                text = content.decode(encoding)
                break
            except (UnicodeDecodeError, UnicodeError):
                continue
        else:
            return DocumentUploadResponse(
                filename=file.filename,
                chunks=0,
                status="encoding_error",
            )

    upload_dir = Path(settings.upload_path)
    upload_dir.mkdir(parents=True, exist_ok=True)
    (upload_dir / file.filename).write_bytes(content)

    documents = chunker.chunk_document(text, metadata={"source": file.filename})
    count = embedding_store.add_documents(documents, user_id=current_user.id)

    return DocumentUploadResponse(
        filename=file.filename,
        chunks=count,
        status="success",
    )


@router.get("/documents/count")
def document_count(
    current_user: User = Depends(get_current_user),
):
    return {"count": embedding_store.get_document_count(user_id=current_user.id)}
