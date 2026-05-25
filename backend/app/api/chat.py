from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session

from app.core.config import settings
from app.core.database import get_db
from app.models.user import User, UserProfile, Conversation, Message
from app.models.schemas import ChatRequest, ChatResponse
from app.rag import embedding_store, llm
from app.api.auth import get_current_user

router = APIRouter()

MAX_HISTORY_MESSAGES = 20


def _build_user_context(profile: UserProfile | None) -> str:
    """将用户画像拼成 prompt 片段"""
    if profile is None:
        return "暂无个人信息。"
    parts = []
    if profile.province:
        parts.append(f"- 省份：{profile.province}")
    if profile.gaokao_score is not None:
        parts.append(f"- 高考分数：{profile.gaokao_score}")
    if profile.gaokao_year is not None:
        parts.append(f"- 高考年份：{profile.gaokao_year}")
    if profile.subject_type:
        parts.append(f"- 选科类型：{profile.subject_type}")
    if profile.interested_majors:
        parts.append(f"- 感兴趣的专业：{profile.interested_majors}")
    return "\n".join(parts) if parts else "暂无个人信息。"


@router.post("/chat", response_model=ChatResponse)
def chat(
    request: ChatRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    try:
        # 1. 获取或创建会话
        if request.conversation_id:
            convo = (
                db.query(Conversation)
                .filter(
                    Conversation.id == request.conversation_id,
                    Conversation.user_id == current_user.id,
                )
                .first()
            )
            if convo is None:
                raise HTTPException(status_code=404, detail="会话不存在")
        else:
            title = request.question[:30]
            convo = Conversation(user_id=current_user.id, title=title)
            db.add(convo)
            db.flush()

        # 2. 检索知识库（使用 user_id 做文档隔离）
        relevant_docs = embedding_store.search(
            request.question, top_k=5, user_id=current_user.id,
        )

        context = "\n\n".join(
            [doc["content"] for doc in relevant_docs]
        ) if relevant_docs else "暂无相关参考信息。"

        # 3. 加载用户画像
        profile = db.query(UserProfile).filter(UserProfile.user_id == current_user.id).first()
        user_context = _build_user_context(profile)

        # 4. 加载历史消息（最近 N 条）
        history_msgs = (
            db.query(Message)
            .filter(Message.conversation_id == convo.id)
            .order_by(Message.created_at.desc())
            .limit(MAX_HISTORY_MESSAGES)
            .all()
        )
        history = [
            {"role": m.role, "content": m.content}
            for m in reversed(history_msgs)
        ]

        # 5. 保存用户消息
        user_msg = Message(
            conversation_id=convo.id,
            role="user",
            content=request.question,
        )
        db.add(user_msg)

        # 6. 调用 LLM
        result = llm.chat(
            question=request.question,
            context=context,
            user_context=user_context,
            history=history,
        )

        # 7. 保存 AI 消息
        sources_data = [
            {
                "content": doc["content"][:200],
                "score": round(doc["score"], 3),
            }
            for doc in relevant_docs
        ]
        assistant_msg = Message(
            conversation_id=convo.id,
            role="assistant",
            content=result["answer"],
            sources=sources_data,
        )
        db.add(assistant_msg)
        db.commit()

        return ChatResponse(
            answer=result["answer"],
            conversation_id=convo.id,
            sources=sources_data,
        )
    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))
