import { createRouter, createWebHistory } from 'vue-router'
import ChatView from '../views/ChatView.vue'
import KnowledgeView from '../views/KnowledgeView.vue'

const routes = [
  { path: '/', name: 'Chat', component: ChatView },
  { path: '/knowledge', name: 'Knowledge', component: KnowledgeView },
]

const router = createRouter({
  history: createWebHistory(),
  routes,
})

export default router
