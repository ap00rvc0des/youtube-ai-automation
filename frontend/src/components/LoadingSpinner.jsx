import React from 'react'
import { motion } from 'framer-motion'
import './LoadingSpinner.css'

function LoadingSpinner({ size = 'md', message = 'Loading...' }) {
  const sizes = {
    sm: 30,
    md: 50,
    lg: 80
  }
  
  return (
    <div className="spinner-container">
      <motion.div
        className="spinner"
        animate={{ rotate: 360 }}
        transition={{ duration: 1, repeat: Infinity, ease: 'linear' }}
        style={{ width: sizes[size], height: sizes[size] }}
      />
      {message && <p className="spinner-message">{message}</p>}
    </div>
  )
}

export default LoadingSpinner
