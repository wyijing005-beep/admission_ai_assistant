from langchain_text_splitters import RecursiveCharacterTextSplitter
from app.core.config import settings


class DocumentChunker:
    def __init__(self):
        self.text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=settings.chunk_size,
            chunk_overlap=settings.chunk_overlap,
            separators=["\n\n", "\n", "。", "！", "？", "；", "，", " ", ""],  #chunk的规则
        )

    def chunk_text(self, text: str) -> list[str]:
        return self.text_splitter.split_text(text)

    def chunk_document(self, text: str, metadata: dict | None = None) -> list[dict]:
        chunks = self.chunk_text(text)
        documents = []
        for i, chunk in enumerate(chunks):
            doc = {
                "content": chunk,
                "metadata": {
                    **(metadata or {}),
                    "chunk_index": i,
                },
            }
            documents.append(doc)
        return documents
