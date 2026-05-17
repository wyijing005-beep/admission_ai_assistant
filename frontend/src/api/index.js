import axios from 'axios'

const api = axios.create({
  baseURL: '/api',
  timeout: 60000,
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
