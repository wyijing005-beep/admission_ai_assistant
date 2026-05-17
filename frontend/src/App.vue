<script setup>
import { useRouter, useRoute } from 'vue-router'

const router = useRouter()
const route = useRoute()
</script>

<template>
  <div class="app-container">
    <header class="app-header">
      <div class="logo" @click="router.push('/')">
        <img src="/logo.png" alt="西安工程大学" class="logo-img" />
        <span>AI 智能问答</span>
      </div>
      <nav class="nav">
        <router-link to="/" :class="{ active: route.path === '/' }">
          智能问答
        </router-link>
        <router-link to="/knowledge" :class="{ active: route.path === '/knowledge' }">
          知识库管理
        </router-link>
      </nav>
    </header>
    <main class="app-main">
      <router-view />
    </main>
  </div>
</template>

<style>
* {
  margin: 0;
  padding: 0;
  box-sizing: border-box;
}

body {
  font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', 'PingFang SC',
    'Hiragino Sans GB', 'Microsoft YaHei', sans-serif;
  background: #f0f2f5;
  color: #333;
}

.app-container {
  display: flex;
  flex-direction: column;
  height: 100vh;
}

.app-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 0 24px;
  height: 60px;
  background: #fff;
  box-shadow: 0 1px 4px rgba(0, 0, 0, 0.08);
  z-index: 100;
}

.logo {
  display: flex;
  align-items: center;
  gap: 10px;
  font-size: 18px;
  color: #1a73e8;
  cursor: pointer;
}

.logo-img {
  height: 36px;
  width: auto;
}

.nav {
  display: flex;
  gap: 16px;
}

.nav a {
  text-decoration: none;
  color: #555;
  padding: 6px 16px;
  border-radius: 6px;
  font-size: 14px;
  transition: all 0.2s;
}

.nav a:hover {
  background: #e8f0fe;
  color: #1a73e8;
}

.nav a.active {
  background: #1a73e8;
  color: #fff;
}

.app-main {
  flex: 1;
  overflow: hidden;
}
</style>
