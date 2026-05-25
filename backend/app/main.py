import os
import json
from pathlib import Path
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.core.config import settings
from app.core.database import engine, Base
from app.api import chat, documents, search, auth, user, conversations
from app.rag import embedding_store, chunker

app = FastAPI(title=settings.app_name, version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(chat.router, prefix="/api", tags=["Chat"])
app.include_router(documents.router, prefix="/api", tags=["Documents"])
app.include_router(search.router, prefix="/api", tags=["Search"])
app.include_router(auth.router, prefix="/api", tags=["Auth"])
app.include_router(user.router, prefix="/api", tags=["User"])
app.include_router(conversations.router, prefix="/api", tags=["Conversations"])


def _load_sources():
    sources_dir = Path(settings.sources_path)
    if not sources_dir.exists():
        return

    manifest_path = Path(settings.vector_store_path) / ".sources_manifest.json"
    loaded = {}
    if manifest_path.exists():
        loaded = json.loads(manifest_path.read_text("utf-8"))

    text_extensions = ("*.txt", "*.md", "*.json", "*.csv", "*.yaml", "*.yml")
    pdf_extensions = ("*.pdf",)
    txt_files = []
    for ext in text_extensions:
        txt_files.extend(sources_dir.rglob(ext))
    pdf_files = []
    for ext in pdf_extensions:
        pdf_files.extend(sources_dir.rglob(ext))
    all_files = sorted(txt_files + pdf_files)
    if not all_files:
        return

    def _read_pdf(file_path: Path) -> str:
        from pypdf import PdfReader
        reader = PdfReader(str(file_path))
        parts = []
        for page in reader.pages:
            text = page.extract_text()
            if text:
                parts.append(text)
        return "\n".join(parts)

    new_count = 0
    for file_path in all_files:
        rel_path = str(file_path.relative_to(sources_dir))
        mtime = os.path.getmtime(file_path)

        if rel_path in loaded and loaded[rel_path] == mtime:
            continue

        if file_path.suffix.lower() == ".pdf":
            try:
                text = _read_pdf(file_path)
            except Exception:
                continue
            if not text.strip():
                continue
        else:
            for encoding in ["utf-8", "gbk", "gb2312"]:
                try:
                    text = file_path.read_text(encoding)
                    break
                except (UnicodeDecodeError, UnicodeError):
                    continue
            else:
                continue

        documents = chunker.chunk_document(text, metadata={"source": rel_path})
        embedding_store.add_documents(documents)
        loaded[rel_path] = mtime
        new_count += 1

    if new_count:
        os.makedirs(settings.vector_store_path, exist_ok=True)
        manifest_path.write_text(json.dumps(loaded, ensure_ascii=False, indent=2), "utf-8")


@app.on_event("startup")
async def startup():
    import app.models.user
    Base.metadata.create_all(bind=engine)
    _load_sources()


@app.get("/")
async def root():
    return {"message": "Local RAG API is running", "docs": "/docs"}


@app.get("/health")
async def health():
    return {"status": "ok"}
