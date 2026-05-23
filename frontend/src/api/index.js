import axios from 'axios'

const SESSION_KEY = 'rag_session_id'

function getSessionId() {
  let id = localStorage.getItem(SESSION_KEY)
  if (!id) {
    id = crypto.randomUUID()
    localStorage.setItem(SESSION_KEY, id)
  }
  return id
}

const api = axios.create({
  baseURL: '/api',
  timeout: 60000,
})

api.interceptors.request.use((config) => {
  config.headers['X-Session-ID'] = getSessionId()
  return config
})

export async function sendChat(question, history = []) {
  const { data } = await api.post('/chat', { question, history })
  return data
}

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

export async function searchDocuments(query, top_k = 5) {
  const { data } = await api.post('/search', { query, top_k })
  return data
}
