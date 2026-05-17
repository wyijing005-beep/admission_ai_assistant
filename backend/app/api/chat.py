from fastapi import APIRouter, HTTPException
from app.models.schemas import ChatRequest, ChatResponse
from app.rag import embedding_store, llm

router = APIRouter()


@router.post("/chat", response_model=ChatResponse)
async def chat(request: ChatRequest):
    try:
        relevant_docs = embedding_store.search(request.question, top_k=5)

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
