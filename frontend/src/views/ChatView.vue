<script setup>
import { ref, nextTick, watch } from 'vue'
import { sendChat, getConversation } from '../api'
import ConversationSidebar from '../components/ConversationSidebar.vue'

const messages = ref([])
const input = ref('')
const loading = ref(false)
const chatBox = ref(null)
const conversationId = ref(null)
const sidebarRef = ref(null)

async function handleSend() {
  const text = input.value.trim()
  if (!text || loading.value) return

  messages.value.push({ role: 'user', content: text })
  input.value = ''
  loading.value = true

  try {
    const res = await sendChat(text, conversationId.value)

    if (!conversationId.value) {
      conversationId.value = res.conversation_id
      sidebarRef.value?.loadList()
    }

    messages.value.push({
      role: 'assistant',
      content: res.answer,
      sources: res.sources || [],
    })
  } catch (e) {
    messages.value.push({
      role: 'assistant',
      content: '抱歉，请求出错了：' + (e.response?.data?.detail || e.message),
    })
  } finally {
    loading.value = false
  }
}

async function selectConversation(id) {
  conversationId.value = id
  loading.value = true
  try {
    const data = await getConversation(id)
    messages.value = data.messages.map(m => ({
      role: m.role,
      content: m.content,
      sources: m.sources || [],
    }))
  } catch {
    messages.value = []
  } finally {
    loading.value = false
  }
}

function newConversation() {
  conversationId.value = null
  messages.value = []
}

function handleKeydown(e) {
  if (e.key === 'Enter' && !e.shiftKey) {
    e.preventDefault()
    handleSend()
  }
}

function selectSuggestion(s) {
  input.value = s
}

watch(messages, async () => {
  await nextTick()
  if (chatBox.value) {
    chatBox.value.scrollTo({ top: chatBox.value.scrollHeight, behavior: 'smooth' })
  }
})
</script>

<template>
  <div class="chat-layout">
    <ConversationSidebar
      ref="sidebarRef"
      :activeId="conversationId"
      @select-conversation="selectConversation"
      @new-conversation="newConversation"
    />
    <div class="chat-root">
      <div class="chat-scroll" ref="chatBox">
        <div v-if="messages.length === 0" class="welcome-screen">
          <div class="welcome-hero">
            <div class="hero-icon">
              <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round">
                <path d="M12 2a4 4 0 0 1 4 4v1h2a2 2 0 0 1 2 2v11a2 2 0 0 1-2 2H6a2 2 0 0 1-2-2V9a2 2 0 0 1 2-2h2V6a4 4 0 0 1 4-4z"/>
                <circle cx="12" cy="14" r="1.2"/>
                <path d="M10 17h4"/>
              </svg>
            </div>
            <h1 class="hero-title">你好，我是校园 AI 助手</h1>
            <p class="hero-desc">
              基于校内招生政策、专业介绍、历年录取数据，<br/>帮你解答志愿填报中的疑问
            </p>
          </div>
          <div class="suggestion-strip">
            <button
              v-for="s in ['计算机专业有什么要求？', '今年招生政策有哪些变化？', '我考了580分能上什么专业？']"
              :key="s"
              @click="selectSuggestion(s)"
              class="suggestion-chip"
            >
              {{ s }}
            </button>
          </div>
        </div>

        <div v-if="messages.length > 0" class="msg-list">
          <div
            v-for="(msg, i) in messages"
            :key="i"
            :class="['msg-row', msg.role]"
          >
            <div class="msg-avatar">
              <template v-if="msg.role === 'user'">
                <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                  <path d="M20 21v-2a4 4 0 0 0-4-4H8a4 4 0 0 0-4 4v2"/>
                  <circle cx="12" cy="7" r="4"/>
                </svg>
              </template>
              <template v-else>
                <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                  <path d="M12 2a4 4 0 0 1 4 4v1h2a2 2 0 0 1 2 2v11a2 2 0 0 1-2 2H6a2 2 0 0 1-2-2V9a2 2 0 0 1 2-2h2V6a4 4 0 0 1 4-4z"/>
                </svg>
              </template>
            </div>
            <div class="msg-body">
              <div class="msg-label">{{ msg.role === 'user' ? '你' : 'AI 助手' }}</div>
              <div class="msg-bubble">
                <div class="msg-text" v-html="msg.content.replace(/\n/g, '<br>')"></div>
              </div>
              <div v-if="msg.sources && msg.sources.length" class="msg-sources">
                <details>
                  <summary>
                    <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="src-icon">
                      <path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"/>
                      <polyline points="14 2 14 8 20 8"/>
                      <line x1="16" y1="13" x2="8" y2="13"/>
                      <line x1="16" y1="17" x2="8" y2="17"/>
                    </svg>
                    参考来源 ({{ msg.sources.length }})
                  </summary>
                  <div class="src-list">
                    <div v-for="(src, j) in msg.sources" :key="j" class="src-item">
                      <span class="src-score">{{ (src.score * 100).toFixed(0) }}%</span>
                      <span class="src-snippet">{{ src.content }}</span>
                    </div>
                  </div>
                </details>
              </div>
            </div>
          </div>
        </div>

        <div v-if="loading" class="msg-row assistant">
          <div class="msg-avatar">
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
              <path d="M12 2a4 4 0 0 1 4 4v1h2a2 2 0 0 1 2 2v11a2 2 0 0 1-2 2H6a2 2 0 0 1-2-2V9a2 2 0 0 1 2-2h2V6a4 4 0 0 1 4-4z"/>
            </svg>
          </div>
          <div class="msg-body">
            <div class="msg-label">AI 助手</div>
            <div class="msg-bubble typing-bubble">
              <span class="typing-dot"></span>
              <span class="typing-dot"></span>
              <span class="typing-dot"></span>
            </div>
          </div>
        </div>
      </div>

      <div class="input-strip">
        <div class="input-row">
          <textarea
            v-model="input"
            placeholder="输入你的问题，按 Enter 发送…"
            :disabled="loading"
            @keydown="handleKeydown"
            rows="1"
          ></textarea>
          <button
            @click="handleSend"
            :disabled="loading || !input.trim()"
            class="send-btn"
            :class="{ ready: input.trim() && !loading }"
          >
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
              <line x1="22" y1="2" x2="11" y2="13"/>
              <polygon points="22 2 15 22 11 13 2 9 22 2"/>
            </svg>
          </button>
        </div>
        <p class="input-hint">回答基于校内知识库，请核对关键信息</p>
      </div>
    </div>
  </div>
</template>

<style scoped>
.chat-layout {
  display: flex;
  height: 100%;
  overflow: hidden;
}

.chat-root {
  display: flex;
  flex-direction: column;
  height: 100%;
  flex: 1;
  max-width: 820px;
  margin: 0 auto;
  width: 100%;
}

.chat-scroll {
  flex: 1;
  overflow-y: auto;
  padding: 28px 24px 12px;
  scroll-behavior: smooth;
}

.welcome-screen {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  height: 100%;
  gap: 36px;
}

.welcome-hero {
  text-align: center;
}

.hero-icon {
  width: 64px;
  height: 64px;
  margin: 0 auto 20px;
  border-radius: 16px;
  background: var(--color-primary-light);
  color: var(--color-primary);
  display: flex;
  align-items: center;
  justify-content: center;
}

.hero-icon svg {
  width: 30px;
  height: 30px;
}

.hero-title {
  font-size: 22px;
  font-weight: 600;
  letter-spacing: -0.02em;
  margin-bottom: 8px;
}

.hero-desc {
  color: var(--color-text-secondary);
  font-size: 14px;
  line-height: 1.7;
}

.suggestion-strip {
  display: flex;
  flex-direction: column;
  gap: 8px;
  width: 100%;
  max-width: 380px;
}

.suggestion-chip {
  width: 100%;
  text-align: left;
  background: var(--color-surface);
  border: 1px solid var(--color-border);
  border-radius: var(--radius-sm);
  padding: 12px 16px;
  font-size: 13px;
  color: var(--color-text-secondary);
  cursor: pointer;
  font-family: inherit;
  transition: all 0.2s ease;
}

.suggestion-chip:hover {
  border-color: var(--color-primary);
  color: var(--color-primary);
  box-shadow: 0 0 0 3px rgba(37, 99, 235, 0.06);
}

.msg-list {
  display: flex;
  flex-direction: column;
  gap: 24px;
}

.msg-row {
  display: flex;
  gap: 12px;
  max-width: 92%;
}

.msg-row.user {
  align-self: flex-end;
  flex-direction: row-reverse;
}

.msg-avatar {
  width: 34px;
  height: 34px;
  border-radius: var(--radius-sm);
  display: flex;
  align-items: center;
  justify-content: center;
  flex-shrink: 0;
  background: #f1f3f6;
  color: var(--color-text-secondary);
}

.msg-avatar svg {
  width: 16px;
  height: 16px;
}

.msg-row.assistant .msg-avatar {
  background: var(--color-primary-light);
  color: var(--color-primary);
}

.msg-label {
  font-size: 11px;
  font-weight: 500;
  color: var(--color-text-muted);
  margin-bottom: 4px;
  padding: 0 2px;
}

.msg-body {
  display: flex;
  flex-direction: column;
  min-width: 0;
}

.msg-row.user .msg-body {
  align-items: flex-end;
}

.msg-bubble {
  background: var(--color-surface);
  padding: 12px 16px;
  border-radius: var(--radius-md);
  box-shadow: var(--shadow-sm);
  border: 1px solid var(--color-border);
  line-height: 1.65;
  font-size: 14px;
}

.msg-row.user .msg-bubble {
  background: var(--color-primary);
  color: #fff;
  border-color: var(--color-primary);
}

.msg-text {
  white-space: pre-wrap;
  word-break: break-word;
}

.msg-sources {
  margin-top: 6px;
  font-size: 12px;
}

.msg-sources summary {
  display: inline-flex;
  align-items: center;
  gap: 4px;
  cursor: pointer;
  color: var(--color-text-muted);
  padding: 4px 8px;
  border-radius: 6px;
  transition: all 0.15s;
  user-select: none;
}

.msg-sources summary:hover {
  background: #f1f3f6;
  color: var(--color-text-secondary);
}

.src-icon {
  width: 13px;
  height: 13px;
}

.src-list {
  margin-top: 8px;
  display: flex;
  flex-direction: column;
  gap: 6px;
}

.src-item {
  display: flex;
  gap: 8px;
  align-items: flex-start;
  padding: 8px 10px;
  background: #f8f9fb;
  border-radius: 6px;
  border: 1px solid var(--color-border);
}

.src-score {
  font-size: 11px;
  font-weight: 600;
  color: var(--color-primary);
  background: var(--color-primary-light);
  padding: 2px 6px;
  border-radius: 4px;
  flex-shrink: 0;
}

.src-snippet {
  font-size: 12px;
  color: var(--color-text-secondary);
  line-height: 1.5;
  word-break: break-all;
}

.typing-bubble {
  display: flex;
  align-items: center;
  gap: 5px;
  padding: 14px 18px !important;
}

.typing-dot {
  width: 7px;
  height: 7px;
  border-radius: 50%;
  background: #c4c8d0;
  animation: dot-pulse 1.3s infinite;
}

.typing-dot:nth-child(2) { animation-delay: 0.18s; }
.typing-dot:nth-child(3) { animation-delay: 0.36s; }

@keyframes dot-pulse {
  0%, 60%, 100% { opacity: 0.3; transform: scale(0.85); }
  30% { opacity: 1; transform: scale(1); }
}

.input-strip {
  padding: 12px 24px 16px;
  background: linear-gradient(180deg, transparent, var(--color-bg) 40%);
}

.input-row {
  display: flex;
  align-items: flex-end;
  gap: 10px;
  background: var(--color-surface);
  border: 1px solid var(--color-border);
  border-radius: var(--radius-md);
  padding: 8px 8px 8px 16px;
  box-shadow: var(--shadow-md);
  transition: border-color 0.2s;
}

.input-row:focus-within {
  border-color: var(--color-primary);
  box-shadow: 0 0 0 3px rgba(37, 99, 235, 0.08), var(--shadow-md);
}

.input-row textarea {
  flex: 1;
  border: none;
  outline: none;
  font-size: 14px;
  font-family: inherit;
  resize: none;
  line-height: 1.5;
  padding: 6px 0;
  max-height: 120px;
  color: var(--color-text);
}

.input-row textarea::placeholder {
  color: var(--color-text-muted);
}

.send-btn {
  width: 38px;
  height: 38px;
  border-radius: var(--radius-sm);
  border: none;
  background: #e5e7eb;
  color: #b0b7c3;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  flex-shrink: 0;
  transition: all 0.2s;
}

.send-btn svg {
  width: 17px;
  height: 17px;
}

.send-btn.ready {
  background: var(--color-primary);
  color: #fff;
}

.send-btn.ready:hover {
  background: var(--color-primary-hover);
}

.send-btn:disabled {
  cursor: not-allowed;
}

.input-hint {
  text-align: center;
  font-size: 11px;
  color: var(--color-text-muted);
  margin-top: 6px;
}
</style>
