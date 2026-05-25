<script setup>
import { ref, onMounted } from 'vue'
import { listConversations, deleteConversation } from '../api'

const emit = defineEmits(['select-conversation', 'new-conversation'])
defineProps(['activeId'])

const conversations = ref([])

async function loadList() {
  try {
    const data = await listConversations()
    conversations.value = data.conversations || []
  } catch {
    // ignore
  }
}

async function handleDelete(id) {
  try {
    await deleteConversation(id)
    conversations.value = conversations.value.filter(c => c.id !== id)
  } catch {
    // ignore
  }
}

function formatDate(iso) {
  if (!iso) return ''
  const d = new Date(iso)
  const now = new Date()
  const diff = now - d
  if (diff < 86400000) {
    return d.toLocaleTimeString('zh-CN', { hour: '2-digit', minute: '2-digit' })
  }
  return d.toLocaleDateString('zh-CN', { month: 'short', day: 'numeric' })
}

onMounted(loadList)

defineExpose({ loadList })
</script>

<template>
  <div class="sidebar">
    <div class="sidebar-head">
      <span class="sidebar-title">历史会话</span>
      <button class="new-btn" @click="emit('new-conversation')">
        <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
          <line x1="12" y1="5" x2="12" y2="19"/>
          <line x1="5" y1="12" x2="19" y2="12"/>
        </svg>
      </button>
    </div>
    <div class="sidebar-list">
      <div
        v-for="c in conversations"
        :key="c.id"
        :class="['sidebar-item', { active: c.id === activeId }]"
        @click="emit('select-conversation', c.id)"
      >
        <div class="item-text">
          <span class="item-title">{{ c.title }}</span>
          <span class="item-date">{{ formatDate(c.created_at) }}</span>
        </div>
        <button class="item-del" @click.stop="handleDelete(c.id)">
          <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
            <line x1="18" y1="6" x2="6" y2="18"/>
            <line x1="6" y1="6" x2="18" y2="18"/>
          </svg>
        </button>
      </div>
      <p v-if="conversations.length === 0" class="sidebar-empty">暂无历史会话</p>
    </div>
  </div>
</template>

<style scoped>
.sidebar {
  width: 260px;
  border-right: 1px solid var(--color-border);
  display: flex;
  flex-direction: column;
  background: #fafbfc;
  flex-shrink: 0;
}

.sidebar-head {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 16px 16px 12px;
}

.sidebar-title {
  font-size: 13px;
  font-weight: 600;
  color: var(--color-text-secondary);
}

.new-btn {
  width: 30px;
  height: 30px;
  border-radius: 6px;
  border: 1px solid var(--color-border);
  background: var(--color-surface);
  color: var(--color-text-secondary);
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: all 0.15s;
}

.new-btn:hover {
  color: var(--color-primary);
  border-color: var(--color-primary);
}

.new-btn svg {
  width: 16px;
  height: 16px;
}

.sidebar-list {
  flex: 1;
  overflow-y: auto;
  padding: 0 12px 12px;
}

.sidebar-item {
  display: flex;
  align-items: center;
  padding: 10px 12px;
  border-radius: var(--radius-sm);
  cursor: pointer;
  transition: background 0.15s;
  margin-bottom: 2px;
}

.sidebar-item:hover {
  background: rgba(0, 0, 0, 0.04);
}

.sidebar-item.active {
  background: var(--color-primary-light);
}

.item-text {
  flex: 1;
  min-width: 0;
  display: flex;
  flex-direction: column;
  gap: 2px;
}

.item-title {
  font-size: 13px;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
  color: var(--color-text);
}

.item-date {
  font-size: 11px;
  color: var(--color-text-muted);
}

.item-del {
  width: 24px;
  height: 24px;
  border: none;
  background: transparent;
  color: var(--color-text-muted);
  cursor: pointer;
  border-radius: 4px;
  display: flex;
  align-items: center;
  justify-content: center;
  opacity: 0;
  transition: all 0.15s;
  flex-shrink: 0;
}

.sidebar-item:hover .item-del {
  opacity: 1;
}

.item-del:hover {
  color: #dc2626;
  background: rgba(220, 38, 38, 0.08);
}

.item-del svg {
  width: 14px;
  height: 14px;
}

.sidebar-empty {
  text-align: center;
  color: var(--color-text-muted);
  font-size: 13px;
  padding: 24px 0;
}
</style>
