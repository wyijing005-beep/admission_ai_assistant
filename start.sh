#!/bin/bash

# 设置 HuggingFace 镜像（国内加速）
export HF_ENDPOINT=https://hf-mirror.com

# 激活 conda 环境并启动后端
echo "Starting backend..."
cd "$(dirname "$0")"
F:/Anaconda_envs/envs/xpu-rag/python.exe -m uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
