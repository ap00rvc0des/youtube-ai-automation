import axios from 'axios'
import { API_BASE_URL } from '../config'

const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json'
  }
})

// Add request interceptor
api.interceptors.request.use(
  config => {
    const token = localStorage.getItem('youtube_token')
    if (token) {
      config.headers.Authorization = `Bearer ${token}`
    }
    return config
  },
  error => Promise.reject(error)
)

// Add response interceptor
api.interceptors.response.use(
  response => response,
  error => {
    if (error.response?.status === 401) {
      localStorage.removeItem('youtube_token')
      window.location.href = '/'
    }
    return Promise.reject(error)
  }
)

export default api
