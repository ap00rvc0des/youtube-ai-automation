export const API_BASE_URL = process.env.REACT_APP_API_URL || 'http://localhost:5000/api'

export const NICHES = [
  'Interesting Facts',
  'History',
  'Technology',
  'Artificial Intelligence',
  'Science',
  'Mystery',
  'Gaming',
  'Automobiles',
  'Finance & Education'
]

export const LANGUAGES = [
  'English',
  'Spanish',
  'French',
  'German',
  'Chinese',
  'Japanese'
]

export const VIDEO_LENGTHS = [
  { label: 'Short (2-3 min)', value: 180 },
  { label: 'Medium (5-7 min)', value: 420 },
  { label: 'Long (10-15 min)', value: 720 }
]
