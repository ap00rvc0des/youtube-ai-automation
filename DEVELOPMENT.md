# 🛠️ Development Guide

Guide for developers wanting to contribute or extend the system.

## Development Environment Setup

```bash
# Clone and setup
git clone https://github.com/ap00rvc0des/youtube-ai-automation.git
cd youtube-ai-automation

# Create virtual environment
python -m venv venv
source venv/bin/activate  # macOS/Linux
venv\Scripts\activate     # Windows

# Install dev dependencies
pip install -r requirements.txt
pip install black flake8 pylint pytest pytest-cov

cd frontend
npm install
cd ..
```

## Project Architecture

### Backend (Python/Flask)

```
backend/
├── app.py              # Flask application
├── pipeline.py         # Video generation pipeline
├── metadata.py         # Metadata management
├── images.py           # Image retrieval
├── subtitles.py        # Subtitle generation
└── routes/
    ├── api.py          # Core API endpoints
    ├── auth.py         # Authentication
    ├── videos.py       # Video management
    └── youtube.py      # YouTube integration
```

### Frontend (React/Vite)

```
frontend/
├── src/
│   ├── main.jsx        # Entry point
│   ├── App.jsx         # Root component
│   ├── pages/          # Page components
│   ├── components/     # Reusable components
│   ├── services/       # API services
│   └── store.js        # State management
└── vite.config.js      # Build configuration
```

### AI Modules

```
ai/
├── llm.py              # Ollama integration
```

```
tts/
├── piper.py            # Piper TTS integration
```

```
video/
├── generator.py        # FFmpeg wrapper
```

```
thumbnails/
├── generator.py        # Pillow-based generator
```

## Code Style

### Python

```bash
# Format with Black
black backend/ ai/ tts/ video/ thumbnails/ youtube/ scheduler/

# Check with Flake8
flake8 backend/ --max-line-length=100

# Lint with Pylint
pylint backend/ --disable=C0103,C0301
```

### JavaScript

```bash
# Format
cd frontend && npm run format

# Lint
cd frontend && npm run lint
```

## Testing

### Run All Tests

```bash
# Python tests
pytest tests/ -v

# With coverage
pytest tests/ --cov=backend --cov-report=html

# Frontend tests
cd frontend && npm run test
```

### Writing Tests

```python
# tests/test_feature.py
import pytest
from backend.module import function

def test_function():
    result = function()
    assert result == expected_value

def test_error_handling():
    with pytest.raises(ValueError):
        function(invalid_input)
```

## Adding New Features

### 1. Add Backend Endpoint

```python
# backend/routes/new_feature.py
from flask import Blueprint, jsonify, request

bp = Blueprint('feature', __name__, url_prefix='/feature')

@bp.route('/action', methods=['POST'])
def action():
    data = request.get_json()
    # Implementation
    return jsonify({'result': 'success'}), 200
```

### 2. Register in app.py

```python
from backend.routes import new_feature
app.register_blueprint(new_feature.bp)
```

### 3. Add Frontend Component

```jsx
// frontend/src/components/Feature.jsx
import React, { useState } from 'react'
import featureService from '../services/featureService'

function Feature() {
  const [loading, setLoading] = useState(false)
  
  const handleClick = async () => {
    setLoading(true)
    try {
      const response = await featureService.action()
      console.log(response)
    } finally {
      setLoading(false)
    }
  }
  
  return (
    <button onClick={handleClick} disabled={loading}>
      {loading ? 'Loading...' : 'Click me'}
    </button>
  )
}

export default Feature
```

### 4. Add Frontend Service

```javascript
// frontend/src/services/featureService.js
import api from './api'

const featureService = {
  action: () => api.post('/feature/action', {})
}

export default featureService
```

### 5. Add Tests

```python
# tests/test_feature.py
import pytest
from backend.app import app

class TestFeature:
    @pytest.fixture
    def client(self):
        app.config['TESTING'] = True
        with app.test_client() as client:
            yield client
    
    def test_action_endpoint(self, client):
        response = client.post('/feature/action')
        assert response.status_code == 200
```

## Common Tasks

### Adding a New Environment Variable

1. Add to `.env.example`
2. Document in `INSTALLATION.md`
3. Use in code: `os.getenv('VARIABLE_NAME', 'default')`

### Adding a New Python Dependency

1. Install locally: `pip install package_name`
2. Add to `requirements.txt`
3. Update version: `pip freeze | grep package_name >> requirements.txt`

### Adding a New JavaScript Dependency

1. Install: `cd frontend && npm install package_name`
2. Update import in component
3. Commit `package-lock.json`

### Running in Debug Mode

```python
# backend/app.py
if __name__ == '__main__':
    app.run(debug=True)
```

## Performance Optimization

### Backend

- Use caching for expensive operations
- Implement pagination for large datasets
- Use background tasks for long operations
- Profile with: `python -m cProfile -s cumulative backend/app.py`

### Frontend

- Code splitting with lazy loading
- Memoize expensive computations
- Optimize bundle size
- Check with: `npm run build -- --analyze`

## Debugging

### Backend Debug Logging

```python
import logging
logger = logging.getLogger(__name__)

logger.debug('Debug message')
logger.info('Info message')
logger.error('Error message')
```

### Frontend Debug

```javascript
console.log('Debug:', value)
console.error('Error:', error)

// React DevTools browser extension recommended
```

## Database Schema (Future)

When moving to a proper database:

```sql
CREATE TABLE videos (
    id TEXT PRIMARY KEY,
    title TEXT NOT NULL,
    description TEXT,
    topic TEXT,
    niche TEXT,
    status TEXT,
    created_at TIMESTAMP,
    updated_at TIMESTAMP
);
```

## Deployment Checklist

- [ ] All tests pass
- [ ] Code formatted (Black/Prettier)
- [ ] Linting passes
- [ ] Documentation updated
- [ ] Environment variables documented
- [ ] No debug logging in production
- [ ] Error handling implemented
- [ ] Performance benchmarked

## Useful Resources

- [Flask Documentation](https://flask.palletsprojects.com/)
- [React Documentation](https://react.dev/)
- [FFmpeg Documentation](https://ffmpeg.org/documentation.html)
- [Ollama API](https://github.com/ollama/ollama/blob/main/docs/api.md)

---

For more info, see CONTRIBUTING.md
