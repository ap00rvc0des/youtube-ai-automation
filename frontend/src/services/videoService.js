import api from './api'

const videoService = {
  generateVideo: (data) => api.post('/videos/generate', data),
  
  getStatus: (videoId) => api.get(`/videos/status/${videoId}`),
  
  listVideos: () => api.get('/videos/list'),
  
  getVideo: (videoId) => api.get(`/videos/${videoId}`),
  
  downloadVideo: (videoId) => api.get(`/videos/${videoId}/download`, {
    responseType: 'blob'
  }),
  
  deleteVideo: (videoId) => api.delete(`/videos/${videoId}`)
}

export default videoService
