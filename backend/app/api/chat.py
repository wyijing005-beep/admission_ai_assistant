from fastapi import APIRouter, HTTPException, Header
from app.models.schemas import ChatRequest, ChatResponse
from app.rag import embedding_store, llm

router = APIRouter()


@router.post("/chat", response_model=ChatResponse)
async def chat(
    request: ChatRequest,
    x_session_id: str | None = Header(default=None, alias="X-Session-ID"),
):
    try:
        relevant_docs = embedding_store.search(
            request.question, top_k=5, session_id=x_session_id,
        )

        context = "\n\n".join(
            [doc["content"] for doc in relevant_docs]
        ) if relevant_docs else "暂无相关参考信息。"

        result = llm.chat(
            question=request.question,
            context=context,
            history=request.history,
        )

        sources = [
            {
                "content": doc["content"][:200],
                "score": round(doc["score"], 3),
            }
            for doc in relevant_docs
        ]

        return ChatResponse(
            answer=result["answer"],
            sources=sources,
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
