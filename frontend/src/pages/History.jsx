import React, { useState, useEffect } from 'react'
import videoService from '../services/videoService'
import './History.css'

function History() {
  const [videos, setVideos] = useState([])
  const [filter, setFilter] = useState('all')
  const [loading, setLoading] = useState(true)
  
  useEffect(() => {
    fetchVideos()
  }, [filter])
  
  const fetchVideos = async () => {
    try {
      setLoading(true)
      const response = await videoService.listVideos()
      setVideos(response.data.videos || [])
    } catch (error) {
      console.error('Error fetching videos:', error)
    } finally {
      setLoading(false)
    }
  }
  
  return (
    <div className="history-page">
      <h2>Video History</h2>
      
      <div className="filter-bar">
        <button
          className={`filter-btn ${filter === 'all' ? 'active' : ''}`}
          onClick={() => setFilter('all')}
        >
          All Videos
        </button>
        <button
          className={`filter-btn ${filter === 'completed' ? 'active' : ''}`}
          onClick={() => setFilter('completed')}
        >
          Completed
        </button>
        <button
          className={`filter-btn ${filter === 'uploaded' ? 'active' : ''}`}
          onClick={() => setFilter('uploaded')}
        >
          Uploaded
        </button>
      </div>
      
      {loading ? (
        <div className="loading">Loading...</div>
      ) : videos.length > 0 ? (
        <div className="videos-table-container">
          <table className="videos-table">
            <thead>
              <tr>
                <th>Title</th>
                <th>Topic</th>
                <th>Created</th>
                <th>Duration</th>
                <th>Status</th>
                <th>Actions</th>
              </tr>
            </thead>
            <tbody>
              {videos.map(video => (
                <tr key={video.id}>
                  <td className="title-cell">{video.title}</td>
                  <td>{video.topic}</td>
                  <td>{new Date(video.created_at).toLocaleDateString()}</td>
                  <td>{video.duration || 'N/A'}</td>
                  <td><span className={`status-badge status-${video.status}`}>{video.status}</span></td>
                  <td>
                    <div className="action-buttons">
                      <button className="action-btn">View</button>
                      <button className="action-btn">Download</button>
                    </div>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      ) : (
        <div className="empty-state">
          <p>No videos found</p>
        </div>
      )}
    </div>
  )
}

export default History
