import os
import pickle
import numpy as np
from typing import Optional
from app.core.config import settings

os.environ.setdefault("HF_ENDPOINT", "https://hf-mirror.com")


class EmbeddingStore:
    def __init__(self):
        self._model = None
        self.documents: list[dict] = []
        self.embeddings: Optional[np.ndarray] = None
        self._load()

    @property
    def model(self):
        if self._model is None:
            from sentence_transformers import SentenceTransformer
            self._model = SentenceTransformer(
                settings.embedding_model_name,
                device=settings.embedding_device,
            )
        return self._model

    def embed(self, texts: list[str]) -> np.ndarray:
        return self.model.encode(texts, normalize_embeddings=True)

    def add_documents(self, documents: list[dict], user_id: int | None = None) -> int:
        texts = [doc["content"] for doc in documents]
        new_embeddings = self.embed(texts)

        start_idx = len(self.documents)
        for i, doc in enumerate(documents):
            doc["id"] = start_idx + i
            doc.setdefault("metadata", {})
            doc["metadata"]["user_id"] = user_id
        self.documents.extend(documents)

        if self.embeddings is None:
            self.embeddings = new_embeddings
        else:
            self.embeddings = np.vstack([self.embeddings, new_embeddings])

        self._save()
        return len(documents)

    def search(self, query: str, top_k: int = 5, user_id: int | None = None) -> list[dict]:
        if not self.documents or self.embeddings is None:
            return []

        query_emb = self.embed([query])
        scores = np.dot(self.embeddings, query_emb.T).flatten()

        fetch_k = min(top_k * 5, len(self.documents))
        top_indices = np.argsort(scores)[::-1][:fetch_k]

        results = []
        for idx in top_indices:
            doc = self.documents[idx]
            doc_user = doc.get("metadata", {}).get("user_id")
            # user_id 为 None 的是公共文档，所有人可见
            if doc_user is not None and doc_user != user_id:
                continue
            if scores[idx] > 0.3:
                results.append({
                    "content": doc["content"],
                    "metadata": doc.get("metadata", {}),
                    "score": float(scores[idx]),
                })
                if len(results) >= top_k:
                    break
        return results

    def _save(self):
        os.makedirs(settings.vector_store_path, exist_ok=True)
        doc_path = os.path.join(settings.vector_store_path, "documents.pkl")
        emb_path = os.path.join(settings.vector_store_path, "embeddings.npy")

        with open(doc_path, "wb") as f:
            pickle.dump(self.documents, f)
        if self.embeddings is not None:
            np.save(emb_path, self.embeddings)

    def _load(self):
        doc_path = os.path.join(settings.vector_store_path, "documents.pkl")
        emb_path = os.path.join(settings.vector_store_path, "embeddings.npy")

        if os.path.exists(doc_path) and os.path.exists(emb_path):
            with open(doc_path, "rb") as f:
                self.documents = pickle.load(f)
            self.embeddings = np.load(emb_path)

    def get_document_count(self, user_id: int | None = None) -> int:
        if user_id is None:
            return len(self.documents)
        return sum(
            1 for d in self.documents
            if d.get("metadata", {}).get("user_id") == user_id
        )

    @property
    def document_count(self) -> int:
        return len(self.documents)
