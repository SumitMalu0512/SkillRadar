import axios from 'axios'

// In dev, vite proxies /api to localhost:5000 (see vite.config.js)
// In production, set VITE_API_URL env var to your Render URL
const baseURL = import.meta.env.VITE_API_URL || ''

export const api = axios.create({
  baseURL,
  timeout: 30000,
  headers: { 'Content-Type': 'application/json' },
})

// global error logging
api.interceptors.response.use(
  res => res,
  err => {
    console.error('[API]', err.response?.status, err.config?.url, err.message)
    return Promise.reject(err)
  }
)

// ---------------- endpoint helpers ----------------

export const jobsAPI = {
  search: (params) => api.get('/api/jobs/search', { params }).then(r => r.data),
  savedData: (params) => api.get('/api/jobs/saved-data', { params }).then(r => r.data),
  ingest: (body) => api.post('/api/jobs/ingest', body).then(r => r.data),
}

export const skillsAPI = {
  top: (limit = 20) => api.get('/api/skills/top', { params: { limit } }).then(r => r.data),
  trending: (limit = 15) => api.get('/api/skills/trending', { params: { limit } }).then(r => r.data),
  emerging: (limit = 10) => api.get('/api/skills/emerging', { params: { limit } }).then(r => r.data),
  declining: (limit = 10) => api.get('/api/skills/declining', { params: { limit } }).then(r => r.data),
  categories: () => api.get('/api/skills/categories').then(r => r.data),
  extract: (text) => api.post('/api/skills/extract', { text }).then(r => r.data),
}

export const clustersAPI = {
  list: () => api.get('/api/clusters').then(r => r.data),
  refresh: (n_clusters = 6) => api.post('/api/clusters/refresh', { n_clusters }).then(r => r.data),
}

export const forecastAPI = {
  forSkill: (skill, days = 90) => api.get(`/api/forecast/${encodeURIComponent(skill)}`, { params: { days } }).then(r => r.data),
  top: (top = 8, days = 90) => api.get('/api/forecast/top/all', { params: { top, days } }).then(r => r.data),
}

export const userAPI = {
  register: (body) => api.post('/api/users/register', body).then(r => r.data),
  saved: (userId) => api.get(`/api/users/${userId}/saved`).then(r => r.data),
  save: (userId, body) => api.post(`/api/users/${userId}/save`, body).then(r => r.data),
  unsave: (userId, jobId) => api.delete(`/api/users/${userId}/save/${jobId}`).then(r => r.data),
}

export const suggestAPI = {
  query: (q, limit = 8) => api.get('/api/suggest', { params: { q, limit } }).then(r => r.data),
}

export const aiAPI = {
  analyzeResume: (file) => {
    const fd = new FormData()
    fd.append('file', file)
    return api.post('/api/ai/resume/analyze', fd, {
      headers: { 'Content-Type': 'multipart/form-data' },
      timeout: 60000,
    }).then(r => r.data)
  },
  tailorResume: (body) => api.post('/api/ai/resume/tailor', body, { timeout: 60000 }).then(r => r.data),
  chat: (message, history = []) => api.post('/api/ai/chat', { message, history }, { timeout: 60000 }).then(r => r.data),
}
