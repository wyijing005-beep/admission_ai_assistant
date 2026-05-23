# 更新日志

## [2026-05-23]

### 重构
- **前端 UI 全面重新设计**：毛玻璃顶栏 + pill 式导航、现代对话气泡、SVG 图标、Inter 字体、CSS 变量设计系统
- **页面过渡动画**：router-view 切换增加淡入淡出效果
- **知识库上传反馈细化**：区分 `success` / `pdf_empty` / `pdf_parse_error` / `encoding_error` 不同状态，展示对应错误提示

### 新增
- **PDF 文件解析支持**：上传接口和 sources 自动加载均支持 `.pdf` 文件，使用 `pypdf.PdfReader` 提取文本
- **文件类型自动识别**：根据文件后缀区分 PDF（二进制解析）与文本文件（编码解码）

### 修复
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
