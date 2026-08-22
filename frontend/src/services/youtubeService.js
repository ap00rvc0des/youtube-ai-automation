import api from './api'

const youtubeService = {
  getChannels: () => api.get('/youtube/channels'),
  
  uploadVideo: (data) => api.post('/youtube/upload', data),
  
  scheduleUpload: (data) => api.post('/youtube/schedule', data)
}

export default youtubeService
