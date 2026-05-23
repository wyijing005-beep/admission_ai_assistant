import os
import io
from pathlib import Path
from fastapi import APIRouter, UploadFile, File
from app.models.schemas import DocumentUploadResponse
from app.rag import embedding_store, chunker
from app.core.config import settings

router = APIRouter()


def _parse_pdf(file_bytes: bytes) -> str:
    """从 PDF 二进制数据中提取文本"""
    from pypdf import PdfReader
    reader = PdfReader(io.BytesIO(file_bytes))
    parts = []
    for page in reader.pages:
        text = page.extract_text()
        if text:
            parts.append(text)
    return "\n".join(parts)


@router.post("/documents/upload", response_model=DocumentUploadResponse)
async def upload_document(file: UploadFile = File(...)):
    content = await file.read()

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
        # 解析纯文本文件（自动检测编码）
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

    # 保存原文件到 uploads/
    upload_dir = Path(settings.upload_path)
    upload_dir.mkdir(parents=True, exist_ok=True)
    (upload_dir / file.filename).write_bytes(content)

    documents = chunker.chunk_document(text, metadata={"source": file.filename})
    count = embedding_store.add_documents(documents)

    return DocumentUploadResponse(
        filename=file.filename,
        chunks=count,
        status="success",
    )


@router.get("/documents/count")
async def document_count():
    return {"count": embedding_store.document_count}
