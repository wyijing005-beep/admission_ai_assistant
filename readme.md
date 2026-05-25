# 某大学 AI 智能问答平台

基于 **DeepSeek 推理引擎** 与 **校内专用知识库** 的智能问答平台，专注解决高考志愿填报中的 **"选专业、看政策、算概率"** 三大难题，让考生提问就有答案、答案就有依据。

---

## 项目概述

本项目是一个面向高校招生场景的 **本地化 RAG（检索增强生成）** 智能问答系统。通过将校内招生政策、专业介绍、历年录取数据等资料进行向量化存储，结合 DeepSeek 大语言模型的推理能力，为考生和家长提供准确、可追溯的志愿填报咨询服务。

## 核心功能

- **选专业** — 基于学生兴趣、分数、选科情况，智能推荐适合的专业
- **看政策** — 精准检索校内最新招生政策、录取规则、加分政策等
- **算概率** — 结合历年录取数据，评估被特定专业录取的可能性
- **检索增强** — 基于 RAG 架构，所有回答均有知识库依据，避免模型幻觉
- **来源追溯** — 每个回答附带参考来源，方便核对原始资料
- **用户系统** — 注册登录、JWT 认证、个人信息（省份/分数/选科）自动融入问答
- **会话管理** — 对话历史自动保存，支持多会话切换和回溯

## 技术栈

| 组件 | 技术选型 |
|------|----------|
| 推理引擎 | DeepSeek (`deepseek-chat`) |
| RAG 框架 | LangChain（文本分割）+ 自研向量存储 |
| 文本嵌入 | BAAI/bge-small-zh-v1.5（Sentence Transformers） |
| 文档切分 | RecursiveCharacterTextSplitter |
| 数据库 | SQLite + SQLAlchemy ORM |
| 认证 | JWT + bcrypt |
| 后端框架 | FastAPI + Uvicorn |
| 前端框架 | Vue 3 + Vite + Vue Router |
| PDF 解析 | pypdf |

## 项目结构

```
Local RAG/
├── backend/                    # 后端服务
│   ├── app/
│   │   ├── api/                # API 路由
│   │   │   ├── auth.py         # 认证接口（注册/登录）
│   │   │   ├── chat.py         # 聊天接口
│   │   │   ├── conversations.py # 会话管理接口
│   │   │   ├── documents.py    # 文档上传接口
│   │   │   ├── search.py       # 知识库搜索接口
│   │   │   └── user.py         # 用户画像接口
│   │   ├── core/
│   │   │   ├── config.py       # 配置管理
│   │   │   └── database.py     # SQLAlchemy 数据库连接
│   │   ├── models/
│   │   │   ├── schemas.py      # Pydantic 请求/响应模型
│   │   │   └── user.py         # ORM 模型（User/Profile/Conversation/Message）
│   │   ├── rag/
│   │   │   ├── chunker.py      # 文档切分模块
│   │   │   ├── embeddings.py   # 向量存储与检索
│   │   │   └── llm.py          # DeepSeek LLM 封装
│   │   └── main.py             # FastAPI 入口
│   ├── data/                   # 数据存储
│   │   ├── sources/            # 预置知识库文档（提交到 Git）
│   │   ├── uploads/            # 用户上传文件（gitignore）
│   │   ├── vector_store/       # 向量库持久化（gitignore）
│   │   └── app.db              # SQLite 数据库（gitignore）
│   ├── .env                    # 环境变量（API Key 等，gitignore）
│   └── .env.example            # 环境变量模板
├── frontend/                   # 前端界面
│   └── src/
│       ├── api/index.js        # Axios 封装 + JWT 拦截器
│       ├── router/index.js     # 路由配置 + 登录守卫
│       ├── components/
│       │   └── ConversationSidebar.vue  # 会话历史侧边栏
│       └── views/
│           ├── ChatView.vue         # 智能问答页
│           ├── KnowledgeView.vue    # 知识库管理页
│           ├── LoginView.vue        # 登录/注册页
│           └── ProfileView.vue      # 个人信息编辑页
├── CHANGELOG.md
└── readme.md
```

## 快速开始

### 1. 配置环境变量

```bash
cp backend/.env.example backend/.env
```

编辑 `backend/.env`，至少填入：

```
DEEPSEEK_API_KEY=你的_DeepSeek_API_Key
JWT_SECRET=自己生成一个随机字符串
```

### 2. 启动后端

```bash
pip install -r backend/requirements.txt

# 国内用户可设置 HuggingFace 镜像加速首次模型下载
export HF_ENDPOINT=https://hf-mirror.com

cd backend
uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
```

后端启动后：
- 自动创建 SQLite 数据库和 4 张表
- 自动加载 `data/sources/` 下的知识库文档到向量库
- 访问 http://localhost:8000/docs 查看 API 文档

### 3. 启动前端

```bash
cd frontend
npm install
npm run dev
```

前端启动后访问 http://localhost:5173 ，首次使用需要注册账号。

## API 接口

| 方法 | 路径 | 说明 | 认证 |
|------|------|------|------|
| POST | `/api/auth/register` | 注册 | 无 |
| POST | `/api/auth/login` | 登录 | 无 |
| POST | `/api/chat` | 发送问题 | JWT |
| GET | `/api/conversations` | 会话列表 | JWT |
| GET | `/api/conversations/{id}` | 会话详情（含消息历史） | JWT |
| DELETE | `/api/conversations/{id}` | 删除会话 | JWT |
| GET | `/api/user/profile` | 获取个人信息 | JWT |
| PUT | `/api/user/profile` | 更新个人信息 | JWT |
| POST | `/api/documents/upload` | 上传文档 | JWT |
| GET | `/api/documents/count` | 文档片段数 | JWT |
| POST | `/api/search` | 知识库检索 | JWT |
| GET | `/health` | 健康检查 | 无 |

## 数据设计

### 关系型数据库（SQLite）

| 表 | 用途 | 核心字段 |
|----|------|----------|
| `users` | 用户账户 | username, password_hash, created_at |
| `user_profiles` | 用户画像 | province, gaokao_score, gaokao_year, subject_type, interested_majors |
| `conversations` | 会话 | user_id, title, created_at |
| `messages` | 消息 | conversation_id, role, content, sources(JSON) |

### 向量存储（NumPy + Pickle）

- `embeddings.npy` — L2 归一化的 embedding 矩阵
- `documents.pkl` — 文档片段列表，含 metadata（source, user_id）
- 检索方式：dot-product 余弦相似度，`top_k × 5` 候选 → session 过滤 → score > 0.3 阈值

### 知识库文档

`backend/data/sources/` 下按类别组织：
- `admissions/` — 历年录取数据
- `majors/` — 专业介绍
- `policies/` — 招生章程与政策

## 开发状态

- [x] RAG 检索流水线
- [x] DeepSeek API 集成
- [x] 知识库管理 + 文档上传（.txt / .md / .pdf）
- [x] 用户注册登录 + JWT 认证
- [x] 用户画像融入问答 Prompt
- [x] 会话持久化 + 多会话管理
- [x] 用户级文档隔离
- [ ] 回答流式输出（SSE）

## 许可证

MIT
