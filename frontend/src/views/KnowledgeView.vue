<script setup>
import { ref, onMounted } from 'vue'
import { uploadDocument, getDocumentCount } from '../api'

const fileCount = ref(0)
const uploading = ref(false)
const uploadStatus = ref('')

async function loadCount() {
  try {
    const res = await getDocumentCount()
    fileCount.value = res.count
  } catch {
    // ignore
  }
}

async function handleUpload(e) {
  const file = e.target.files[0]
  if (!file) return

  uploading.value = true
  uploadStatus.value = `正在上传 ${file.name}...`

  try {
    const res = await uploadDocument(file)
    uploadStatus.value = `✅ 上传成功：${res.filename}（${res.chunks} 个文档块）`
    await loadCount()
  } catch (err) {
    uploadStatus.value = `❌ 上传失败：${err.response?.data?.detail || err.message}`
  } finally {
    uploading.value = false
    e.target.value = ''
  }
}
</script>

<template>
  <div class="knowledge-container">
    <div class="page-header">
      <h2>📚 知识库管理</h2>
      <p>上传校内招生政策、专业介绍等文档，构建专属知识库</p>
    </div>

    <div class="stats-card">
      <div class="stat-item">
        <span class="stat-number">{{ fileCount }}</span>
        <span class="stat-label">文档片段数</span>
      </div>
    </div>

    <div class="upload-card">
      <h3>上传文档</h3>
      <p class="hint">支持 .txt 格式文件（后续将支持 PDF）</p>

      <label class="upload-btn" :class="{ disabled: uploading }">
        <input
          type="file"
          accept=".txt,.md,.pdf"
          @change="handleUpload"
          :disabled="uploading"
          hidden
        />
        <span>{{ uploading ? '上传中...' : '选择文件上传' }}</span>
      </label>

      <div v-if="uploadStatus" class="status-msg">{{ uploadStatus }}</div>
    </div>

    <div class="tips-card">
      <h3>💡 使用建议</h3>
      <ul>
        <li>上传招生章程、专业介绍等政策文件</li>
        <li>上传历年录取分数线数据</li>
        <li>上传常见问题 FAQ 文档</li>
        <li>文件内容越清晰，回答越准确</li>
      </ul>
    </div>
  </div>
</template>

<style scoped>
.knowledge-container {
  max-width: 700px;
  margin: 0 auto;
  padding: 32px 24px;
  overflow-y: auto;
  height: 100%;
}

.page-header {
  margin-bottom: 24px;
}

.page-header h2 {
  font-size: 22px;
  margin-bottom: 8px;
}

.page-header p {
  color: #666;
  font-size: 14px;
}

.stats-card {
  background: #fff;
  border-radius: 12px;
  padding: 24px;
  margin-bottom: 16px;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.08);
}

.stat-item {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 4px;
}

.stat-number {
  font-size: 36px;
  font-weight: 700;
  color: #1a73e8;
}

.stat-label {
  font-size: 14px;
  color: #888;
}

.upload-card {
  background: #fff;
  border-radius: 12px;
  padding: 24px;
  margin-bottom: 16px;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.08);
}

.upload-card h3 {
  margin-bottom: 8px;
}

.hint {
  color: #999;
  font-size: 13px;
  margin-bottom: 16px;
}

.upload-btn {
  display: inline-block;
  padding: 10px 24px;
  background: #1a73e8;
  color: #fff;
  border-radius: 8px;
  cursor: pointer;
  font-size: 14px;
  transition: background 0.2s;
}

.upload-btn:hover {
  background: #1557b0;
}

.upload-btn.disabled {
  background: #ccc;
  cursor: not-allowed;
}

.status-msg {
  margin-top: 12px;
  padding: 10px 14px;
  background: #f6f8fa;
  border-radius: 8px;
  font-size: 13px;
  color: #333;
}

.tips-card {
  background: #fff;
  border-radius: 12px;
  padding: 24px;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.08);
}

.tips-card h3 {
  margin-bottom: 12px;
}

.tips-card ul {
  list-style: none;
  padding: 0;
}

.tips-card li {
  padding: 6px 0;
  color: #555;
  font-size: 14px;
}

.tips-card li::before {
  content: '• ';
  color: #1a73e8;
}
</style>
