import React, { useState } from 'react'
import './Settings.css'

function Settings() {
  const [settings, setSettings] = useState({
    defaultNiche: 'Technology',
    defaultLanguage: 'English',
    defaultVideoLength: '420',
    youtubeEnabled: false,
    schedulerEnabled: false,
    schedulerTime: '09:00',
    schedulerFrequency: 'daily'
  })
  
  const [saved, setSaved] = useState(false)
  
  const handleSettingChange = (key, value) => {
    setSettings(prev => ({
      ...prev,
      [key]: value
    }))
  }
  
  const handleSave = () => {
    // Save settings to localStorage or API
    localStorage.setItem('appSettings', JSON.stringify(settings))
    setSaved(true)
    setTimeout(() => setSaved(false), 2000)
  }
  
  return (
    <div className="settings-page">
      <h2>Settings</h2>
      
      <div className="settings-container">
        <div className="settings-section">
          <h3>Default Generation Settings</h3>
          
          <div className="setting-item">
            <label>Default Niche</label>
            <select
              value={settings.defaultNiche}
              onChange={(e) => handleSettingChange('defaultNiche', e.target.value)}
              className="select"
            >
              <option>Technology</option>
              <option>Science</option>
              <option>History</option>
              <option>AI</option>
            </select>
          </div>
          
          <div className="setting-item">
            <label>Default Language</label>
            <select
              value={settings.defaultLanguage}
              onChange={(e) => handleSettingChange('defaultLanguage', e.target.value)}
              className="select"
            >
              <option>English</option>
              <option>Spanish</option>
              <option>French</option>
            </select>
          </div>
          
          <div className="setting-item">
            <label>Default Video Length</label>
            <select
              value={settings.defaultVideoLength}
              onChange={(e) => handleSettingChange('defaultVideoLength', e.target.value)}
              className="select"
            >
              <option value="180">Short (2-3 min)</option>
              <option value="420">Medium (5-7 min)</option>
              <option value="720">Long (10-15 min)</option>
            </select>
          </div>
        </div>
        
        <div className="settings-section">
          <h3>YouTube Integration</h3>
          
          <div className="setting-item toggle-item">
            <label>Enable YouTube Upload</label>
            <input
              type="checkbox"
              checked={settings.youtubeEnabled}
              onChange={(e) => handleSettingChange('youtubeEnabled', e.target.checked)}
              className="toggle"
            />
          </div>
          
          {settings.youtubeEnabled && (
            <div className="info-box">
              <p>Configure your YouTube OAuth credentials in the environment setup</p>
            </div>
          )}
        </div>
        
        <div className="settings-section">
          <h3>Auto-Scheduler</h3>
          
          <div className="setting-item toggle-item">
            <label>Enable Scheduler</label>
            <input
              type="checkbox"
              checked={settings.schedulerEnabled}
              onChange={(e) => handleSettingChange('schedulerEnabled', e.target.checked)}
              className="toggle"
            />
          </div>
          
          {settings.schedulerEnabled && (
            <>
              <div className="setting-item">
                <label>Schedule Time</label>
                <input
                  type="time"
                  value={settings.schedulerTime}
                  onChange={(e) => handleSettingChange('schedulerTime', e.target.value)}
                  className="input"
                />
              </div>
              
              <div className="setting-item">
                <label>Frequency</label>
                <select
                  value={settings.schedulerFrequency}
                  onChange={(e) => handleSettingChange('schedulerFrequency', e.target.value)}
                  className="select"
                >
                  <option value="daily">Daily</option>
                  <option value="weekly">Weekly</option>
                  <option value="monthly">Monthly</option>
                </select>
              </div>
            </>
          )}
        </div>
        
        <div className="settings-section">
          <h3>System Information</h3>
          <div className="info-grid">
            <div className="info-item">
              <span className="label">Backend Status:</span>
              <span className="value">🟢 Connected</span>
            </div>
            <div className="info-item">
              <span className="label">Ollama Status:</span>
              <span className="value">🟢 Available</span>
            </div>
            <div className="info-item">
              <span className="label">Piper TTS Status:</span>
              <span className="value">🟢 Available</span>
            </div>
            <div className="info-item">
              <span className="label">FFmpeg Status:</span>
              <span className="value">🟢 Installed</span>
            </div>
          </div>
        </div>
        
        <div className="settings-actions">
          <button className="btn btn-primary" onClick={handleSave}>
            Save Settings
          </button>
          {saved && <span className="save-message">✓ Settings saved</span>}
        </div>
      </div>
    </div>
  )
}

export default Settings
