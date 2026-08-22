import api from './api'

const authService = {
  checkStatus: () => api.get('/auth/status'),
  
  youtubeLogin: () => api.get('/auth/youtube/login'),
  
  logout: () => api.post('/auth/logout'),
  
  getChannels: () => api.get('/youtube/channels')
}

export default authService
