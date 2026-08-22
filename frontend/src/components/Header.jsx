import React from 'react'
import './Header.css'

function Header() {
  return (
    <header className="header">
      <div className="header-content">
        <div className="logo">
          <h1>🎬 YouTube AI Automation</h1>
        </div>
        <div className="header-actions">
          <button className="btn btn-secondary">Settings</button>
          <button className="btn btn-secondary">Help</button>
        </div>
      </div>
    </header>
  )
}

export default Header
