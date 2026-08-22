import React, { useState } from 'react'
import './ProgressBar.css'

function ProgressBar({ progress = 0, steps = [] }) {
  return (
    <div className="progress-container">
      <div className="progress-bar">
        <div
          className="progress-fill"
          style={{ width: `${progress}%` }}
        />
      </div>
      <p className="progress-text">{progress}% Complete</p>
      {steps.length > 0 && (
        <div className="steps">
          {steps.map((step, index) => (
            <div key={index} className={`step ${step.status}`}>
              <span className="step-icon">
                {step.status === 'completed' && '✓'}
                {step.status === 'current' && '⏳'}
                {step.status === 'pending' && '○'}
              </span>
              <span className="step-label">{step.label}</span>
            </div>
          ))}
        </div>
      )}
    </div>
  )
}

export default ProgressBar
