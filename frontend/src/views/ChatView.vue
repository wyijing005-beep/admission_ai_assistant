<script setup>
import { ref, nextTick } from 'vue'
import { sendChat } from '../api'

const messages = ref([])
const input = ref('')
const loading = ref(false)
const chatBox = ref(null)

async function handleSend() {
  const text = input.value.trim()
  if (!text || loading.value) return

  messages.value.push({ role: 'user', content: text })
  input.value = ''
  loading.value = true

  try {
    const history = messages.value.map(m => ({
      role: m.role,
      content: m.content,
    }))

    const res = await sendChat(text, history.slice(-10))

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

function handleKeydown(e) {
  if (e.key === 'Enter' && !e.shiftKey) {
    e.preventDefault()
    handleSend()
  }
}
</script>

<template>
  <div class="chat-container">
    <div class="chat-messages" ref="chatBox">
      <div v-if="messages.length === 0" class="welcome">
        <div class="welcome-icon">💬</div>
        <h2>欢迎使用 AI 智能问答</h2>
        <p>西安工程大学 AI 智能助手，帮你解答关于专业选择、招生政策、录取概率等问题</p>
        <div class="suggestions">
          <button
            v-for="s in ['计算机专业有什么要求？', '今年招生政策有哪些变化？', '我考了580分能上什么专业？']"
            :key="s"
            @click="input = s"
          >
            {{ s }}
          </button>
        </div>
      </div>

      <div
        v-for="(msg, i) in messages"
        :key="i"
        :class="['message', msg.role]"
      >
        <div class="avatar">{{ msg.role === 'user' ? '👤' : '🤖' }}</div>
        <div class="bubble">
          <div class="text" v-html="msg.content.replace(/\n/g, '<br>')"></div>
          <div v-if="msg.sources && msg.sources.length" class="sources">
            <details>
              <summary>📎 参考来源 ({{ msg.sources.length }})</summary>
              <div v-for="(src, j) in msg.sources" :key="j" class="source-item">
                <span class="score">[{{ src.score }}]</span>
                {{ src.content }}
              </div>
            </details>
          </div>
        </div>
      </div>

      <div v-if="loading" class="message assistant">
        <div class="avatar">🤖</div>
        <div class="bubble">
          <div class="typing">思考中<span>.</span><span>.</span><span>.</span></div>
        </div>
      </div>
    </div>

    <div class="chat-input">
      <textarea
        v-model="input"
        placeholder="输入你的问题..."
        :disabled="loading"
        @keydown="handleKeydown"
        rows="2"
      ></textarea>
      <button @click="handleSend" :disabled="loading || !input.trim()">
        发送
      </button>
    </div>
  </div>
</template>

<style scoped>
.chat-container {
  display: flex;
  flex-direction: column;
  height: 100%;
  max-width: 900px;
  margin: 0 auto;
  width: 100%;
}

.chat-messages {
  flex: 1;
  overflow-y: auto;
  padding: 24px;
  display: flex;
  flex-direction: column;
  gap: 16px;
}

.welcome {
  text-align: center;
  margin: auto;
  color: #888;
}

.welcome-icon {
  font-size: 48px;
  margin-bottom: 12px;
}

.welcome h2 {
  color: #333;
  margin-bottom: 8px;
}

.suggestions {
  display: flex;
  flex-direction: column;
  gap: 8px;
  margin-top: 24px;
  align-items: center;
}

.suggestions button {
  background: #fff;
  border: 1px solid #ddd;
  border-radius: 20px;
  padding: 10px 20px;
  cursor: pointer;
  font-size: 14px;
  color: #1a73e8;
  transition: all 0.2s;
  max-width: 400px;
}

.suggestions button:hover {
  background: #e8f0fe;
  border-color: #1a73e8;
}

.message {
  display: flex;
  gap: 12px;
  max-width: 85%;
}

.message.user {
  align-self: flex-end;
  flex-direction: row-reverse;
}

.avatar {
  width: 36px;
  height: 36px;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 18px;
  flex-shrink: 0;
}

.bubble {
  background: #fff;
  padding: 12px 16px;
  border-radius: 12px;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.08);
  line-height: 1.6;
}

.message.user .bubble {
  background: #1a73e8;
  color: #fff;
}

.text {
  white-space: pre-wrap;
  word-break: break-word;
}

.sources {
  margin-top: 8px;
  padding-top: 8px;
  border-top: 1px solid #eee;
  font-size: 13px;
}

.message.user .sources {
  border-top-color: rgba(255, 255, 255, 0.2);
}

.sources summary {
  cursor: pointer;
  color: #666;
  font-size: 12px;
}

.source-item {
  padding: 4px 0;
  color: #555;
  font-size: 12px;
}

.source-item .score {
  color: #1a73e8;
  font-weight: 500;
}

.typing span {
  animation: blink 1.4s infinite;
  animation-fill-mode: both;
}

.typing span:nth-child(2) {
  animation-delay: 0.2s;
}

.typing span:nth-child(3) {
  animation-delay: 0.4s;
}

@keyframes blink {
  0%, 80% { opacity: 0; }
  40% { opacity: 1; }
}

.chat-input {
  display: flex;
  gap: 12px;
  padding: 16px 24px;
  background: #fff;
  border-top: 1px solid #eee;
}

.chat-input textarea {
  flex: 1;
  border: 1px solid #ddd;
  border-radius: 8px;
  padding: 10px 14px;
  font-size: 14px;
  resize: none;
  outline: none;
  font-family: inherit;
  transition: border-color 0.2s;
}

.chat-input textarea:focus {
  border-color: #1a73e8;
}

.chat-input button {
  padding: 10px 24px;
  background: #1a73e8;
  color: #fff;
  border: none;
  border-radius: 8px;
  font-size: 14px;
  cursor: pointer;
  transition: background 0.2s;
  align-self: flex-end;
}

.chat-input button:hover:not(:disabled) {
  background: #1557b0;
}

.chat-input button:disabled {
  background: #ccc;
  cursor: not-allowed;
}
</style>
