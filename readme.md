# 西安工程大学 AI 智能问答平台

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

## 技术栈

| 组件 | 技术选型 |
|------|----------|
| 推理引擎 | DeepSeek 官方 API |
| RAG 框架 | LangChain |
| 向量数据库 | FAISS（本地） |
| 文本嵌入 | BAAI/bge-small-zh-v1.5 |
| 文档切分 | RecursiveCharacterTextSplitter |
| 后端框架 | FastAPI + Uvicorn |
| 前端框架 | Vue 3 + Vite |
| 环境管理 | Conda |

## 项目结构

```
Local RAG/
├── backend/                # 后端服务
│   ├── app/
│   │   ├── api/            # API 路由
│   │   │   ├── chat.py     # 聊天接口
│   │   │   ├── documents.py # 文档上传接口
│   │   │   └── search.py   # 知识库搜索接口
│   │   ├── core/
│   │   │   └── config.py   # 配置管理
│   │   ├── models/
│   │   │   └── schemas.py  # Pydantic 数据模型
│   │   ├── rag/
│   │   │   ├── chunker.py  # 文档切分模块
│   │   │   ├── embeddings.py # 向量化与向量存储
│   │   │   └── llm.py      # DeepSeek LLM 封装
│   │   └── main.py         # FastAPI 入口
│   ├── data/               # 数据存储（上传文件、向量库）
│   ├── .env                # 环境变量（API Key 等）
│   └── .env.example        # 环境变量模板
├── frontend/               # 前端界面
│   └── src/
│       ├── api/            # API 调用封装
│       ├── router/         # 路由配置
│       └── views/          # 页面组件
│           ├── ChatView.vue    # 智能问答页
│           └── KnowledgeView.vue # 知识库管理页
├── start.sh                # 后端启动脚本
├── start_frontend.sh       # 前端启动脚本
└── readme.md
```

## 快速开始

### 1. 配置环境变量

```bash
# 复制环境变量模板
cp backend/.env.example backend/.env

# 编辑 backend/.env，填入你的 DeepSeek API Key
DEEPSEEK_API_KEY=your_api_key_here
```

### 2. 启动后端

```bash
# 使用 Conda 环境
conda activate xpu-rag

# 设置 HuggingFace 镜像（国内访问加速）
export HF_ENDPOINT=https://hf-mirror.com

# 启动后端服务
uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
```

或者直接运行启动脚本（Windows Git Bash）：

```bash
./start.sh
```

后端启动后访问 http://localhost:8000/docs 查看 API 文档。

### 3. 启动前端

```bash
cd frontend
npm install
npm run dev
```

前端启动后访问 http://localhost:5173 即可使用。

## API 接口

| 方法 | 路径 | 说明 |
|------|------|------|
| POST | `/api/chat` | 发送问题，获取回答 |
| POST | `/api/documents/upload` | 上传知识库文档 |
| GET | `/api/documents/count` | 查询文档片段数 |
| POST | `/api/search` | 检索知识库 |
| GET | `/health` | 健康检查 |

## 开发状态

- [x] 项目基础搭建
- [x] 后端 FastAPI 框架搭建
- [x] 前端 Vue 3 项目初始化
- [x] RAG 检索流水线
- [x] DeepSeek API 集成
- [x] 智能问答页面
- [x] 知识库管理页面
- [ ] 文档上传与自动切分
- [ ] 回答流式输出
- [ ] 用户会话管理

## 许可证

MIT
