from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import desc

from app.core.database import get_db
from app.models.user import User, Conversation, Message
from app.models.schemas import (
    ConversationListResponse,
    ConversationItem,
    ConversationDetailResponse,
    MessageItem,
)
from app.api.auth import get_current_user

router = APIRouter()


@router.get("/conversations", response_model=ConversationListResponse)
def list_conversations(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    convos = (
        db.query(Conversation)
        .filter(Conversation.user_id == current_user.id)
        .order_by(desc(Conversation.created_at))
        .all()
    )
    items = [
        ConversationItem(
            id=c.id,
            title=c.title,
            created_at=c.created_at.isoformat() if c.created_at else "",
        )
        for c in convos
    ]
    return ConversationListResponse(conversations=items)


@router.get("/conversations/{conversation_id}", response_model=ConversationDetailResponse)
def get_conversation(
    conversation_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    convo = (
        db.query(Conversation)
        .filter(Conversation.id == conversation_id, Conversation.user_id == current_user.id)
        .first()
    )
    if convo is None:
        raise HTTPException(status_code=404, detail="会话不存在")

    msgs = (
        db.query(Message)
        .filter(Message.conversation_id == conversation_id)
        .order_by(Message.created_at)
        .all()
    )

    return ConversationDetailResponse(
        id=convo.id,
        title=convo.title,
        messages=[
            MessageItem(
                id=m.id,
                role=m.role,
                content=m.content,
                sources=m.sources,
                created_at=m.created_at.isoformat() if m.created_at else "",
            )
            for m in msgs
        ],
    )


@router.delete("/conversations/{conversation_id}")
def delete_conversation(
    conversation_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    convo = (
        db.query(Conversation)
        .filter(Conversation.id == conversation_id, Conversation.user_id == current_user.id)
        .first()
    )
    if convo is None:
        raise HTTPException(status_code=404, detail="会话不存在")

    db.query(Message).filter(Message.conversation_id == conversation_id).delete()
    db.delete(convo)
    db.commit()
    return {"detail": "已删除"}
