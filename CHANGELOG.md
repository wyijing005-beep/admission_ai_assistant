# 更新日志

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
