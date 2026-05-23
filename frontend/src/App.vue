<script setup>
import { useRouter, useRoute } from 'vue-router'

const router = useRouter()
const route = useRoute()
</script>

<template>
  <div class="app-shell">
    <header class="topbar">
      <div class="topbar-inner">
        <div class="brand" @click="router.push('/')">
          <div class="brand-icon">
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round">
              <path d="M22 10v6M2 10l10-5 10 5-10 5z"/>
              <path d="M6 12v5c0 2 4 3 6 3s6-1 6-3v-5"/>
            </svg>
          </div>
          <span class="brand-text">AI 智能问答</span>
        </div>
        <nav class="topbar-nav">
          <router-link to="/" :class="['nav-pill', { active: route.path === '/' }]">
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="nav-icon">
              <path d="M21 15a2 2 0 0 1-2 2H7l-4 4V5a2 2 0 0 1 2-2h14a2 2 0 0 1 2 2z"/>
            </svg>
            智能问答
          </router-link>
          <router-link to="/knowledge" :class="['nav-pill', { active: route.path === '/knowledge' }]">
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="nav-icon">
              <path d="M4 19.5A2.5 2.5 0 0 1 6.5 17H20"/>
              <path d="M6.5 2H20v20H6.5A2.5 2.5 0 0 1 4 19.5v-15A2.5 2.5 0 0 1 6.5 2z"/>
            </svg>
            知识库
          </router-link>
        </nav>
      </div>
    </header>
    <main class="main-stage">
      <router-view v-slot="{ Component }">
        <transition name="page-fade" mode="out-in">
          <component :is="Component" />
        </transition>
      </router-view>
    </main>
  </div>
</template>

<style>
*,
*::before,
*::after {
  margin: 0;
  padding: 0;
  box-sizing: border-box;
}

:root {
  --color-bg: #f6f7fa;
  --color-surface: #ffffff;
  --color-border: #e8ecf1;
  --color-text: #1a1d23;
  --color-text-secondary: #6b7280;
  --color-text-muted: #9ca3af;
  --color-primary: #2563eb;
  --color-primary-light: #eff4ff;
  --color-primary-hover: #1d4ed8;
  --radius-sm: 8px;
  --radius-md: 12px;
  --radius-lg: 16px;
  --shadow-sm: 0 1px 2px rgba(0, 0, 0, 0.04);
  --shadow-md: 0 4px 16px rgba(0, 0, 0, 0.06);
}

body {
  font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', 'PingFang SC',
    'Hiragino Sans GB', 'Microsoft YaHei', sans-serif;
  background: var(--color-bg);
  color: var(--color-text);
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
}

.app-shell {
  display: flex;
  flex-direction: column;
  height: 100vh;
  overflow: hidden;
}

/* ---- Topbar ---- */
.topbar {
  background: rgba(255, 255, 255, 0.82);
  backdrop-filter: blur(16px);
  -webkit-backdrop-filter: blur(16px);
  border-bottom: 1px solid var(--color-border);
  position: sticky;
  top: 0;
  z-index: 100;
}

.topbar-inner {
  display: flex;
  align-items: center;
  justify-content: space-between;
  max-width: 1100px;
  margin: 0 auto;
  padding: 0 24px;
  height: 56px;
}

.brand {
  display: flex;
  align-items: center;
  gap: 10px;
  cursor: pointer;
  user-select: none;
}

.brand-icon {
  width: 34px;
  height: 34px;
  border-radius: var(--radius-sm);
  background: linear-gradient(135deg, #2563eb, #3b82f6);
  color: #fff;
  display: flex;
  align-items: center;
  justify-content: center;
}

.brand-icon svg {
  width: 18px;
  height: 18px;
}

.brand-text {
  font-size: 16px;
  font-weight: 600;
  color: var(--color-text);
  letter-spacing: -0.01em;
}

/* ---- Navigation ---- */
.topbar-nav {
  display: flex;
  gap: 6px;
  background: #f1f3f6;
  padding: 4px;
  border-radius: 10px;
}

.nav-pill {
  display: flex;
  align-items: center;
  gap: 6px;
  text-decoration: none;
  color: var(--color-text-secondary);
  font-size: 13px;
  font-weight: 500;
  padding: 7px 16px;
  border-radius: 7px;
  transition: all 0.2s ease;
}

.nav-pill:hover {
  color: var(--color-text);
  background: rgba(255, 255, 255, 0.6);
}

.nav-pill.active {
  background: #fff;
  color: var(--color-primary);
  box-shadow: var(--shadow-sm);
}

.nav-icon {
  width: 15px;
  height: 15px;
}

/* ---- Main ---- */
.main-stage {
  flex: 1;
  overflow: hidden;
  display: flex;
  flex-direction: column;
}

/* ---- Page transition ---- */
.page-fade-enter-active,
.page-fade-leave-active {
  transition: opacity 0.18s ease;
}

.page-fade-enter-from,
.page-fade-leave-to {
  opacity: 0;
}
</style>
