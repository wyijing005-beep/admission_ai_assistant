from fastapi import APIRouter, Header
from app.models.schemas import SearchRequest, SearchResponse
from app.rag import embedding_store

router = APIRouter()


@router.post("/search", response_model=SearchResponse)
async def search(
    request: SearchRequest,
    x_session_id: str | None = Header(default=None, alias="X-Session-ID"),
):
    results = embedding_store.search(
        request.query, top_k=request.top_k, session_id=x_session_id,
    )
    return SearchResponse(results=results, total=len(results))
