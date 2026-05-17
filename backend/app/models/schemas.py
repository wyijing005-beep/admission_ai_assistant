from pydantic import BaseModel, Field
from typing import Optional, List


class ChatRequest(BaseModel):
    question: str = Field(..., description="用户问题")
    history: Optional[List[dict]] = Field(default=None, description="历史消息")


class ChatResponse(BaseModel):
    answer: str
    sources: List[dict] = []
    reasoning: Optional[str] = None


class DocumentUploadResponse(BaseModel):
    filename: str
    chunks: int
    status: str


class SearchRequest(BaseModel):
    query: str
    top_k: int = 5


class SearchResponse(BaseModel):
    results: List[dict]
    total: int
