import React, { useState, useEffect } from 'react'
import videoService from '../services/videoService'
import './Dashboard.css'

function Dashboard() {
  const [stats, setStats] = useState({
    totalVideos: 0,
    videosThisMonth: 0,
    totalMinutes: 0,
    uploadedToYouTube: 0
  })
  
  const [recentVideos, setRecentVideos] = useState([])
  
  useEffect(() => {
    fetchDashboardData()
  }, [])
  
  const fetchDashboardData = async () => {
    try {
      const response = await videoService.listVideos()
      // Parse response and update stats
      setRecentVideos(response.data.videos || [])
    } catch (error) {
      console.error('Error fetching dashboard data:', error)
    }
  }
  
  return (
    <div className="dashboard-page">
      <h2>Dashboard</h2>
      
      <div className="stats-grid">
        <div className="stat-card">
          <div className="stat-icon">🎬</div>
          <div className="stat-content">
            <h3>Total Videos</h3>
            <p className="stat-value">{stats.totalVideos}</p>
          </div>
        </div>
        
        <div className="stat-card">
          <div className="stat-icon">📅</div>
          <div className="stat-content">
            <h3>This Month</h3>
            <p className="stat-value">{stats.videosThisMonth}</p>
          </div>
        </div>
        
        <div className="stat-card">
          <div className="stat-icon">⏱️</div>
          <div className="stat-content">
            <h3>Total Minutes</h3>
            <p className="stat-value">{stats.totalMinutes}</p>
          </div>
        </div>
        
        <div className="stat-card">
          <div className="stat-icon">📤</div>
          <div className="stat-content">
            <h3>Uploaded</h3>
            <p className="stat-value">{stats.uploadedToYouTube}</p>
          </div>
        </div>
      </div>
      
      <div className="recent-videos">
        <h3>Recent Videos</h3>
        {recentVideos.length > 0 ? (
          <div className="videos-list">
            {recentVideos.map(video => (
              <div key={video.id} className="video-item">
                <div className="video-thumbnail">🎬</div>
                <div className="video-info">
                  <h4>{video.title}</h4>
                  <p>{video.created_at}</p>
                </div>
                <div className="video-status">
                  <span className={`badge badge-${video.status}`}>{video.status}</span>
                </div>
              </div>
            ))}
          </div>
        ) : (
          <div className="empty-state">
            <p>No videos yet. Start by <a href="/generate">generating a video</a></p>
          </div>
        )}
      </div>
    </div>
  )
}

export default Dashboard
