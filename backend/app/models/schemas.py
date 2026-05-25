from pydantic import BaseModel, Field
from typing import Optional, List


# ── Chat ──

class ChatRequest(BaseModel):
    question: str = Field(..., description="用户问题")
    conversation_id: Optional[int] = Field(default=None, description="会话ID")


class ChatResponse(BaseModel):
    answer: str
    conversation_id: int
    sources: List[dict] = []


# ── Auth ──

class RegisterRequest(BaseModel):
    username: str = Field(..., min_length=2, max_length=64, description="用户名")
    password: str = Field(..., min_length=6, max_length=128, description="密码")


class LoginRequest(BaseModel):
    username: str = Field(..., description="用户名")
    password: str = Field(..., description="密码")


class AuthResponse(BaseModel):
    token: str
    user_id: int
    username: str


# ── User Profile ──

class UserProfileRequest(BaseModel):
    province: Optional[str] = Field(default=None, description="省份")
    gaokao_score: Optional[float] = Field(default=None, description="高考分数")
    gaokao_year: Optional[int] = Field(default=None, description="高考年份")
    subject_type: Optional[str] = Field(default=None, description="选科类型")
    interested_majors: Optional[str] = Field(default=None, description="感兴趣的专业")


class UserProfileResponse(BaseModel):
    province: Optional[str] = None
    gaokao_score: Optional[float] = None
    gaokao_year: Optional[int] = None
    subject_type: Optional[str] = None
    interested_majors: Optional[str] = None


# ── Conversation ──

class ConversationItem(BaseModel):
    id: int
    title: str
    created_at: str


class ConversationListResponse(BaseModel):
    conversations: List[ConversationItem]


class MessageItem(BaseModel):
    id: int
    role: str
    content: str
    sources: Optional[List[dict]] = None
    created_at: str


class ConversationDetailResponse(BaseModel):
    id: int
    title: str
    messages: List[MessageItem]


# ── Document ──

class DocumentUploadResponse(BaseModel):
    filename: str
    chunks: int
    status: str


# ── Search ──

class SearchRequest(BaseModel):
    query: str
    top_k: int = 5


class SearchResponse(BaseModel):
    results: List[dict]
    total: int
