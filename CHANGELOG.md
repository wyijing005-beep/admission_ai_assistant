# 更新日志

## [2026-05-23]

### 前端重构
- **前端 UI 全面重新设计**：毛玻璃顶栏 + pill 式导航、现代对话气泡、SVG 图标、Inter 字体、CSS 变量设计系统
- **页面过渡动画**：router-view 切换增加淡入淡出效果
- **知识库上传反馈细化**：区分 `success` / `pdf_empty` / `pdf_parse_error` / `encoding_error` 不同状态，展示对应错误提示
- **Session 隔离（前端）**：`api/index.js` 生成持久化 UUID，axios 拦截器自动注入 `X-Session-ID` header

### 新增后端功能
- **PDF 文件解析支持**：上传接口和 sources 自动加载均支持 `.pdf` 文件，使用 `pypdf.PdfReader` 提取文本
- **文件类型自动识别**：根据文件后缀区分 PDF（二进制解析）与文本文件（编码解码）
- **用户文档隔离**：基于 `X-Session-ID` header 的 session 级隔离，用户上传文档仅自己可见，sources 公共文档全员可见
  - `EmbeddingStore` 三大方法均支持 `session_id` 参数
  - 检索取 `top_k × 5` 候选 → 过滤 → 截断，兼顾精度与隔离
  - 向后兼容：旧向量库无 `session_id` 字段的文档自动视为公共

### 调整
- **LLM 温度参数调整**：`temperature` 从 0.7 降至 0.5，提高问答稳定性

## [2026-05-17]

### 重构
- **目录职责划分**：明确了 `data/sources/`（开发者原始资料）和 `data/uploads/`（用户上传文件）的分工
- **启动自动加载**：`main.py` 新增 `_load_sources()`，服务启动时自动扫描 `data/sources/` 下所有文本文件，加载到向量库
- **支持多种文件格式**：sources 和 uploads 均支持 `.txt`、`.md`、`.json`、`.csv`、`.yaml`、`.yml`
- **编码自动检测**：读取文件时自动尝试 UTF-8 → GBK → GB2312，避免乱码

### 修复
- **配置路径集中管理**：`config.py` 新增 `sources_path`、`upload_path`，去除各模块中硬编码的路径

### 增强
- **HuggingFace 镜像加速**：`embeddings.py` 设置 `HF_ENDPOINT` 为 `hf-mirror.com`，解决国内下载模型慢的问题
- **加载清单机制**：通过 `.sources_manifest.json` 追踪已加载的文件，避免重复加载

### 杂项
- 初始化 git 仓库，添加 `.gitignore` 排除缓存文件和敏感配置
