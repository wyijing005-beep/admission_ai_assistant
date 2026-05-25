import axios from 'axios'

const TOKEN_KEY = 'rag_token'

function getToken() {
  return localStorage.getItem(TOKEN_KEY)
}

export function setToken(token) {
  localStorage.setItem(TOKEN_KEY, token)
}

export function clearToken() {
  localStorage.removeItem(TOKEN_KEY)
}

export function isLoggedIn() {
  return !!getToken()
}

const api = axios.create({
  baseURL: '/api',
  timeout: 60000,
})

api.interceptors.request.use((config) => {
  const token = getToken()
  if (token) {
    config.headers['Authorization'] = `Bearer ${token}`
  }
  return config
})

api.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.response?.status === 401) {
      clearToken()
    }
    return Promise.reject(error)
  }
)

// ── Auth ──

export async function register(username, password) {
  const { data } = await api.post('/auth/register', { username, password })
  setToken(data.token)
  return data
}

export async function login(username, password) {
  const { data } = await api.post('/auth/login', { username, password })
  setToken(data.token)
  return data
}

export function logout() {
  clearToken()
}

// ── Chat ──

export async function sendChat(question, conversationId = null) {
  const { data } = await api.post('/chat', { question, conversation_id: conversationId })
  return data
}

// ── Documents ──

export async function uploadDocument(file) {
  const form = new FormData()
  form.append('file', file)
  const { data } = await api.post('/documents/upload', form)
  return data
}

export async function getDocumentCount() {
  const { data } = await api.get('/documents/count')
  return data
}

// ── Search ──

export async function searchDocuments(query, top_k = 5) {
  const { data } = await api.post('/search', { query, top_k })
  return data
}

// ── User Profile ──

export async function getProfile() {
  const { data } = await api.get('/user/profile')
  return data
}

export async function updateProfile(profile) {
  const { data } = await api.put('/user/profile', profile)
  return data
}

// ── Conversations ──

export async function listConversations() {
  const { data } = await api.get('/conversations')
  return data
}

export async function getConversation(id) {
  const { data } = await api.get(`/conversations/${id}`)
  return data
}

export async function deleteConversation(id) {
  const { data } = await api.delete(`/conversations/${id}`)
  return data
}
