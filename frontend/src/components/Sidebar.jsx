import React from 'react'
import { Link, useLocation } from 'react-router-dom'
import './Sidebar.css'

function Sidebar() {
  const location = useLocation()
  
  const isActive = (path) => location.pathname === path
  
  return (
    <aside className="sidebar">
      <nav className="nav">
        <Link
          to="/"
          className={`nav-item ${isActive('/') ? 'active' : ''}`}
        >
          <span className="icon">📊</span>
          <span>Dashboard</span>
        </Link>
        <Link
          to="/generate"
          className={`nav-item ${isActive('/generate') ? 'active' : ''}`}
        >
          <span className="icon">🎬</span>
          <span>Generate Video</span>
        </Link>
        <Link
          to="/history"
          className={`nav-item ${isActive('/history') ? 'active' : ''}`}
        >
          <span className="icon">📜</span>
          <span>History</span>
        </Link>
        <Link
          to="/settings"
          className={`nav-item ${isActive('/settings') ? 'active' : ''}`}
        >
          <span className="icon">⚙️</span>
          <span>Settings</span>
        </Link>
      </nav>
    </aside>
  )
}

export default Sidebar
