import React, { useState, useEffect } from 'react'
import videoService from '../services/videoService'
import useStore from '../store'
import LoadingSpinner from '../components/LoadingSpinner'
import ProgressBar from '../components/ProgressBar'
import { NICHES, LANGUAGES, VIDEO_LENGTHS } from '../config'
import './Generator.css'

function Generator() {
  const [formData, setFormData] = useState({
    topic: '',
    niche: 'Technology',
    language: 'English',
    videoLength: 420,
    voice: 'en_US-lessac-medium'
  })
  
  const { isGenerating, generationProgress, setIsGenerating, setGenerationProgress } = useStore()
  const [generatedScript, setGeneratedScript] = useState('')
  const [currentStep, setCurrentStep] = useState('')
  
  const steps = [
    { label: 'Generating Script', status: generationProgress > 0 ? 'completed' : generationProgress === 0 && isGenerating ? 'current' : 'pending' },
    { label: 'Creating Voiceover', status: generationProgress > 20 ? 'completed' : generationProgress > 0 && isGenerating ? 'current' : 'pending' },
    { label: 'Generating Visuals', status: generationProgress > 40 ? 'completed' : generationProgress > 20 && isGenerating ? 'current' : 'pending' },
    { label: 'Editing Video', status: generationProgress > 60 ? 'completed' : generationProgress > 40 && isGenerating ? 'current' : 'pending' },
    { label: 'Adding Subtitles', status: generationProgress > 80 ? 'completed' : generationProgress > 60 && isGenerating ? 'current' : 'pending' },
    { label: 'Finalizing', status: generationProgress > 90 ? 'completed' : generationProgress > 80 && isGenerating ? 'current' : 'pending' }
  ]
  
  const handleInputChange = (e) => {
    const { name, value } = e.target
    setFormData(prev => ({
      ...prev,
      [name]: value
    }))
  }
  
  const handleGenerateClick = async (e) => {
    e.preventDefault()
    
    if (!formData.topic.trim()) {
      alert('Please enter a video topic')
      return
    }
    
    setIsGenerating(true)
    setGenerationProgress(0)
    
    try {
      const response = await videoService.generateVideo({
        topic: formData.topic,
        niche: formData.niche,
        language: formData.language,
        video_length: formData.videoLength,
        voice: formData.voice
      })
      
      // Simulate progress for demo
      const interval = setInterval(() => {
        setGenerationProgress(prev => {
          if (prev >= 100) {
            clearInterval(interval)
            setIsGenerating(false)
            return 100
          }
          return prev + Math.random() * 15
        })
      }, 2000)
      
    } catch (error) {
      console.error('Generation error:', error)
      alert('Error generating video')
      setIsGenerating(false)
    }
  }
  
  return (
    <div className="generator-page">
      <div className="generator-container">
        <h2>Generate YouTube Video</h2>
        
        {!isGenerating ? (
          <form className="generator-form" onSubmit={handleGenerateClick}>
            <div className="form-group">
              <label htmlFor="topic">Video Topic *</label>
              <input
                type="text"
                id="topic"
                name="topic"
                value={formData.topic}
                onChange={handleInputChange}
                placeholder="e.g., The Future of AI in 2024"
                className="input"
              />
            </div>
            
            <div className="form-row">
              <div className="form-group">
                <label htmlFor="niche">Niche</label>
                <select
                  id="niche"
                  name="niche"
                  value={formData.niche}
                  onChange={handleInputChange}
                  className="select"
                >
                  {NICHES.map(niche => (
                    <option key={niche} value={niche}>{niche}</option>
                  ))}
                </select>
              </div>
              
              <div className="form-group">
                <label htmlFor="language">Language</label>
                <select
                  id="language"
                  name="language"
                  value={formData.language}
                  onChange={handleInputChange}
                  className="select"
                >
                  {LANGUAGES.map(lang => (
                    <option key={lang} value={lang}>{lang}</option>
                  ))}
                </select>
              </div>
            </div>
            
            <div className="form-row">
              <div className="form-group">
                <label htmlFor="videoLength">Video Length</label>
                <select
                  id="videoLength"
                  name="videoLength"
                  value={formData.videoLength}
                  onChange={handleInputChange}
                  className="select"
                >
                  {VIDEO_LENGTHS.map(length => (
                    <option key={length.value} value={length.value}>{length.label}</option>
                  ))}
                </select>
              </div>
              
              <div className="form-group">
                <label htmlFor="voice">Voice</label>
                <select
                  id="voice"
                  name="voice"
                  value={formData.voice}
                  onChange={handleInputChange}
                  className="select"
                >
                  <option value="en_US-lessac-medium">Lessac (Male)</option>
                  <option value="en_US-libritts-high">LibriTTS (Female)</option>
                  <option value="en_GB-alba-medium">Alba (British)</option>
                </select>
              </div>
            </div>
            
            <button type="submit" className="btn btn-primary btn-large">
              Generate Video
            </button>
          </form>
        ) : (
          <div className="generation-progress">
            <LoadingSpinner message="Generating your video..." />
            <ProgressBar progress={Math.min(generationProgress, 100)} steps={steps} />
          </div>
        )}
      </div>
    </div>
  )
}

export default Generator
