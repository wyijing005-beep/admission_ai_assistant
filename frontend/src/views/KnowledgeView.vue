<script setup>
import { ref, onMounted } from 'vue'
import { uploadDocument, getDocumentCount } from '../api'

const fileCount = ref(0)
const uploading = ref(false)
const uploadStatus = ref('')
const statusType = ref('')

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
  uploadStatus.value = `正在上传 ${file.name}…`
  statusType.value = 'info'

  try {
    const res = await uploadDocument(file)
    if (res.status === 'success' && res.chunks > 0) {
      uploadStatus.value = `上传成功：${res.filename}（${res.chunks} 个片段）`
      statusType.value = 'success'
    } else if (res.status === 'pdf_empty') {
      uploadStatus.value = `⚠️ ${res.filename} 可能是扫描版 PDF（纯图片），无法提取文字。请使用文字型 PDF 或直接复制内容到 txt 文件上传。`
      statusType.value = 'error'
    } else if (res.status === 'pdf_parse_error') {
      uploadStatus.value = `❌ ${res.filename} PDF 解析失败，文件可能已损坏或格式不兼容。`
      statusType.value = 'error'
    } else if (res.status === 'encoding_error') {
      uploadStatus.value = `❌ ${res.filename} 编码无法识别，请转换为 UTF-8 格式后重试。`
      statusType.value = 'error'
    } else {
      uploadStatus.value = `⚠️ ${res.filename} 上传完成但未提取到内容（${res.chunks} 个片段）`
      statusType.value = 'error'
    }
    await loadCount()
  } catch (err) {
    uploadStatus.value = `上传失败：${err.response?.data?.detail || err.message}`
    statusType.value = 'error'
  } finally {
    uploading.value = false
    e.target.value = ''
  }
}

onMounted(() => {
  loadCount()
})
</script>

<template>
  <div class="kb-root">
    <div class="kb-page">
      <div class="kb-hero">
        <h2>知识库管理</h2>
        <p>上传校内招生政策、专业介绍等文档，构建专属知识库。上传后立即可在问答中使用。</p>
      </div>

      <!-- Stats -->
      <div class="stat-card">
        <div class="stat-ring">
          <svg viewBox="0 0 36 36" class="ring-bg">
            <path d="M18 2.0845 a 15.9155 15.9155 0 0 1 0 31.831 a 15.9155 15.9155 0 0 1 0 -31.831" fill="none" stroke="#e8ecf1" stroke-width="3"/>
            <path d="M18 2.0845 a 15.9155 15.9155 0 0 1 0 31.831" fill="none" stroke="#2563eb" stroke-width="3" stroke-dasharray="75, 100" stroke-linecap="round"/>
          </svg>
          <span class="ring-value">{{ fileCount }}</span>
        </div>
        <div class="stat-info">
          <span class="stat-label">已索引文档片段</span>
          <span class="stat-hint">片段越多，回答覆盖越全面</span>
        </div>
      </div>

      <!-- Upload -->
      <div class="card upload-card">
        <div class="card-header">
          <h3>上传新文档</h3>
          <span class="card-badge">.txt .md .pdf</span>
        </div>
        <div class="upload-dropzone">
          <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round" class="upload-icon">
            <path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4"/>
            <polyline points="17 8 12 3 7 8"/>
            <line x1="12" y1="3" x2="12" y2="15"/>
          </svg>
          <p class="upload-prompt">拖拽文件到此处，或点击下方按钮选择文件</p>
          <label :class="['upload-btn', { disabled: uploading }]">
            <input
              type="file"
              accept=".txt,.md,.pdf"
              @change="handleUpload"
              :disabled="uploading"
              hidden
            />
            <span>{{ uploading ? '上传中…' : '选择文件' }}</span>
          </label>
        </div>
        <transition name="fade">
          <div v-if="uploadStatus" :class="['upload-toast', statusType]">
            <template v-if="statusType === 'success'">
              <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="toast-icon">
                <path d="M22 11.08V12a10 10 0 1 1-5.93-9.14"/>
                <polyline points="22 4 12 14.01 9 11.01"/>
              </svg>
            </template>
            <template v-else-if="statusType === 'error'">
              <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="toast-icon">
                <circle cx="12" cy="12" r="10"/>
                <line x1="15" y1="9" x2="9" y2="15"/>
                <line x1="9" y1="9" x2="15" y2="15"/>
              </svg>
            </template>
            <span>{{ uploadStatus }}</span>
          </div>
        </transition>
      </div>

      <!-- Tips -->
      <div class="card tips-card">
        <h3>推荐上传内容</h3>
        <div class="tips-grid">
          <div class="tip-item">
            <div class="tip-dot"></div>
            <div>
              <strong>招生章程</strong>
              <p>录取规则、加分政策、体检要求等官方文件</p>
            </div>
          </div>
          <div class="tip-item">
            <div class="tip-dot"></div>
            <div>
              <strong>专业介绍</strong>
              <p>各专业的培养方向、课程设置、就业前景</p>
            </div>
          </div>
          <div class="tip-item">
            <div class="tip-dot"></div>
            <div>
              <strong>历年录取数据</strong>
              <p>各省份、各专业的录取分数线与位次</p>
            </div>
          </div>
          <div class="tip-item">
            <div class="tip-dot"></div>
            <div>
              <strong>常见问题 FAQ</strong>
              <p>高频咨询问题的标准答复</p>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<style scoped>
.kb-root {
  height: 100%;
  overflow-y: auto;
}

.kb-page {
  max-width: 640px;
  margin: 0 auto;
  padding: 36px 24px 48px;
  display: flex;
  flex-direction: column;
  gap: 20px;
}

/* ---- Hero ---- */
.kb-hero h2 {
  font-size: 20px;
  font-weight: 600;
  letter-spacing: -0.02em;
  margin-bottom: 6px;
}

.kb-hero p {
  font-size: 13px;
  color: var(--color-text-secondary);
  line-height: 1.6;
}

/* ---- Card ---- */
.card {
  background: var(--color-surface);
  border: 1px solid var(--color-border);
  border-radius: var(--radius-lg);
  padding: 24px;
  box-shadow: var(--shadow-sm);
}

.card-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-bottom: 20px;
}

.card-header h3 {
  font-size: 15px;
  font-weight: 600;
}

.card-badge {
  font-size: 11px;
  color: var(--color-text-muted);
  background: #f1f3f6;
  padding: 3px 10px;
  border-radius: 20px;
  font-weight: 500;
}

/* ---- Stat ---- */
.stat-card {
  background: var(--color-surface);
  border: 1px solid var(--color-border);
  border-radius: var(--radius-lg);
  padding: 24px;
  box-shadow: var(--shadow-sm);
  display: flex;
  align-items: center;
  gap: 20px;
}

.stat-ring {
  position: relative;
  width: 72px;
  height: 72px;
  flex-shrink: 0;
}

.ring-bg {
  width: 100%;
  height: 100%;
}

.ring-value {
  position: absolute;
  inset: 0;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 24px;
  font-weight: 700;
  color: var(--color-primary);
}

.stat-info {
  display: flex;
  flex-direction: column;
  gap: 2px;
}

.stat-label {
  font-size: 14px;
  font-weight: 500;
}

.stat-hint {
  font-size: 12px;
  color: var(--color-text-muted);
}

/* ---- Upload ---- */
.upload-dropzone {
  border: 2px dashed var(--color-border);
  border-radius: var(--radius-md);
  padding: 32px 24px;
  text-align: center;
  transition: border-color 0.2s;
}

.upload-dropzone:hover {
  border-color: var(--color-primary);
}

.upload-icon {
  width: 36px;
  height: 36px;
  color: var(--color-text-muted);
  margin-bottom: 12px;
}

.upload-prompt {
  font-size: 13px;
  color: var(--color-text-muted);
  margin-bottom: 16px;
}

.upload-btn {
  display: inline-flex;
  align-items: center;
  padding: 9px 22px;
  background: var(--color-primary);
  color: #fff;
  border-radius: var(--radius-sm);
  font-size: 13px;
  font-weight: 500;
  cursor: pointer;
  transition: background 0.2s;
}

.upload-btn:hover {
  background: var(--color-primary-hover);
}

.upload-btn.disabled {
  background: #c4c8d0;
  cursor: not-allowed;
}

.upload-toast {
  margin-top: 14px;
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 10px 14px;
  border-radius: var(--radius-sm);
  font-size: 13px;
}

.upload-toast.success {
  background: #ecfdf5;
  color: #065f46;
}

.upload-toast.error {
  background: #fef2f2;
  color: #991b1b;
}

.upload-toast.info {
  background: #eff4ff;
  color: #1e40af;
}

.toast-icon {
  width: 16px;
  height: 16px;
  flex-shrink: 0;
}

/* ---- Tips ---- */
.tips-card h3 {
  font-size: 15px;
  font-weight: 600;
  margin-bottom: 18px;
}

.tips-grid {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 14px;
}

.tip-item {
  display: flex;
  gap: 10px;
}

.tip-dot {
  width: 6px;
  height: 6px;
  border-radius: 50%;
  background: var(--color-primary);
  margin-top: 6px;
  flex-shrink: 0;
}

.tip-item strong {
  font-size: 13px;
  font-weight: 500;
  display: block;
  margin-bottom: 2px;
}

.tip-item p {
  font-size: 12px;
  color: var(--color-text-secondary);
  line-height: 1.5;
}

/* ---- Transitions ---- */
.fade-enter-active,
.fade-leave-active {
  transition: opacity 0.25s ease;
}

.fade-enter-from,
.fade-leave-to {
  opacity: 0;
}
</style>
