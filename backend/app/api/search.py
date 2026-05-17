from fastapi import APIRouter
from app.models.schemas import SearchRequest, SearchResponse
from app.rag import embedding_store

router = APIRouter()


@router.post("/search", response_model=SearchResponse)
async def search(request: SearchRequest):
    results = embedding_store.search(request.query, top_k=request.top_k)
    return SearchResponse(results=results, total=len(results))
