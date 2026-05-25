from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.models.schemas import SearchRequest, SearchResponse
from app.models.user import User
from app.rag import embedding_store
from app.core.database import get_db
from app.api.auth import get_current_user

router = APIRouter()


@router.post("/search", response_model=SearchResponse)
def search(
    request: SearchRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    results = embedding_store.search(
        request.query, top_k=request.top_k, user_id=current_user.id,
    )
    return SearchResponse(results=results, total=len(results))
