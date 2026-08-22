# 📚 API Documentation

## Base URL

```
http://localhost:5000/api
```

## Authentication

Currently no API authentication required for local use. For YouTube upload features, OAuth2 is required.

---

## Endpoints

### Core API

#### Get System Status
```
GET /api/status
```

**Response:**
```json
{
  "status": "operational",
  "services": {
    "llm": "configured",
    "tts": "configured",
    "video_encoder": "available",
    "thumbnail_generator": "available"
  }
}
```

#### Get Available Niches
```
GET /api/niches
```

**Response:**
```json
{
  "niches": [
    "Interesting Facts",
    "History",
    "Technology",
    "Artificial Intelligence",
    "Science",
    "Mystery",
    "Gaming",
    "Automobiles",
    "Finance & Education"
  ],
  "count": 9
}
```

#### Get Configuration
```
GET /api/config
```

**Response:**
```json
{
  "ollama_available": true,
  "piper_available": true,
  "ffmpeg_available": true,
  "youtube_oauth_configured": false
}
```

---

### Video Generation

#### Start Video Generation
```
POST /videos/generate
Content-Type: application/json
```

**Request Body:**
```json
{
  "topic": "The Future of Artificial Intelligence",
  "niche": "Artificial Intelligence",
  "language": "English",
  "video_length": 420,
  "voice": "en_US-lessac-medium"
}
```

**Parameters:**
| Parameter | Type | Required | Description | Default |
|-----------|------|----------|-------------|---------|
| topic | string | Yes | Video topic | - |
| niche | string | No | Video category | "Technology" |
| language | string | No | Script language | "English" |
| video_length | integer | No | Duration in seconds | 420 |
| voice | string | No | TTS voice model | "en_US-lessac-medium" |

**Response (202 Accepted):**
```json
{
  "video_id": "video_20240822_101234_a1b2c3d4",
  "status": "processing",
  "progress": 0,
  "topic": "The Future of Artificial Intelligence",
  "niche": "Artificial Intelligence",
  "language": "English"
}
```

#### Get Video Generation Status
```
GET /videos/status/{video_id}
```

**Response:**
```json
{
  "video_id": "video_20240822_101234_a1b2c3d4",
  "status": "processing",
  "progress": 45,
  "current_step": "Creating Video"
}
```

**Status Values:**
- `processing` - Video is being generated
- `completed` - Video generation finished
- `failed` - An error occurred

#### List All Videos
```
GET /videos/list
```

**Response:**
```json
{
  "videos": [
    {
      "video_id": "video_20240822_101234_a1b2c3d4",
      "filename": "video_20240822_101234_a1b2c3d4.mp4",
      "file_size": 524288000,
      "file_size_mb": 500.0,
      "created_at": "2024-08-22T10:12:34.123456",
      "status": "completed",
      "title": "The Future of Artificial Intelligence",
      "topic": "The Future of Artificial Intelligence",
      "duration": 420
    }
  ],
  "total": 1
}
```

#### Get Video Details
```
GET /videos/{video_id}
```

**Response:**
```json
{
  "video_id": "video_20240822_101234_a1b2c3d4",
  "filename": "video_20240822_101234_a1b2c3d4.mp4",
  "file_size": 524288000,
  "file_size_mb": 500.0,
  "created_at": "2024-08-22T10:12:34.123456",
  "status": "completed",
  "download_url": "/videos/video_20240822_101234_a1b2c3d4/download",
  "title": "The Future of Artificial Intelligence",
  "description": "Learn about the future of AI...",
  "topic": "The Future of Artificial Intelligence",
  "niche": "Artificial Intelligence",
  "language": "English",
  "duration": 420,
  "thumbnail": "/storage/thumbnails/video_20240822_101234_a1b2c3d4.png",
  "script": "/storage/video_20240822_101234_a1b2c3d4_script.txt"
}
```

#### Download Video
```
GET /videos/{video_id}/download
```

**Response:** Binary MP4 file

#### Delete Video
```
DELETE /videos/{video_id}
```

**Response:**
```json
{
  "message": "Video deleted successfully"
}
```

---

### Authentication

#### Check Authentication Status
```
GET /auth/status
```

**Response:**
```json
{
  "authenticated": false,
  "providers": {
    "youtube": false
  }
}
```

#### YouTube Login
```
GET /auth/youtube/login
```

**Response:** Redirects to Google OAuth consent screen

#### YouTube Callback
```
GET /auth/youtube/callback?code={auth_code}&state={state}
```

#### Logout
```
POST /auth/logout
```

**Response:**
```json
{
  "message": "Logged out successfully"
}
```

---

### YouTube Integration

#### Get User Channels
```
GET /youtube/channels
Authorization: Bearer {token}
```

**Response:**
```json
{
  "channels": [
    {
      "id": "UC1234567890abcdef",
      "title": "My Channel",
      "description": "Channel description",
      "subscriber_count": 1000,
      "video_count": 50
    }
  ]
}
```

#### Upload Video to YouTube
```
POST /youtube/upload
Authorization: Bearer {token}
Content-Type: application/json
```

**Request Body:**
```json
{
  "video_id": "video_20240822_101234_a1b2c3d4",
  "channel_id": "UC1234567890abcdef",
  "title": "The Future of Artificial Intelligence",
  "description": "Learn about the future of AI...",
  "tags": ["AI", "technology", "future"],
  "privacy_status": "private",
  "category_id": "28"
}
```

**Parameters:**
| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| video_id | string | Yes | Generated video ID |
| channel_id | string | Yes | YouTube channel ID |
| title | string | Yes | Video title (max 100 chars) |
| description | string | Yes | Video description |
| tags | array | No | Video tags |
| privacy_status | string | No | 'public', 'private', 'unlisted' |
| category_id | string | No | YouTube category ID |

**Response:**
```json
{
  "video_id": "dQw4w9WgXcQ",
  "title": "The Future of Artificial Intelligence",
  "url": "https://youtube.com/watch?v=dQw4w9WgXcQ",
  "status": "uploaded"
}
```

#### Schedule Video Upload
```
POST /youtube/schedule
Authorization: Bearer {token}
Content-Type: application/json
```

**Request Body:**
```json
{
  "video_id": "video_20240822_101234_a1b2c3d4",
  "channel_id": "UC1234567890abcdef",
  "title": "The Future of Artificial Intelligence",
  "description": "Learn about the future of AI...",
  "publish_time": "2024-08-23T18:00:00Z",
  "privacy_status": "private"
}
```

**Response:**
```json
{
  "scheduled_for": "2024-08-23T18:00:00Z",
  "video_id": "video_20240822_101234_a1b2c3d4",
  "status": "scheduled"
}
```

---

## Error Responses

### 400 Bad Request
```json
{
  "error": "Missing required field: topic"
}
```

### 404 Not Found
```json
{
  "error": "Video not found"
}
```

### 500 Internal Server Error
```json
{
  "error": "Failed to generate video",
  "message": "Detailed error message"
}
```

---

## Rate Limiting

No rate limiting for local installation. For production deployment, rate limiting is recommended.

---

## CORS

CORS is enabled for all origins in development mode. For production, configure allowed origins in backend.

---

## WebSocket Support (Coming Soon)

Real-time progress updates via WebSocket:
```
ws://localhost:5000/ws/videos/{video_id}/progress
```

---

## Code Examples

### cURL

```bash
# Generate video
curl -X POST http://localhost:5000/videos/generate \
  -H "Content-Type: application/json" \
  -d '{
    "topic": "The Future of AI",
    "niche": "Artificial Intelligence",
    "language": "English"
  }'

# Check status
curl http://localhost:5000/videos/status/video_20240822_101234_a1b2c3d4

# Download video
curl -O http://localhost:5000/videos/video_20240822_101234_a1b2c3d4/download
```

### Python

```python
import requests

# Generate video
response = requests.post('http://localhost:5000/videos/generate', json={
    'topic': 'The Future of AI',
    'niche': 'Artificial Intelligence',
    'language': 'English'
})
video_id = response.json()['video_id']

# Check status
status = requests.get(f'http://localhost:5000/videos/status/{video_id}')
print(status.json())
```

### JavaScript

```javascript
// Generate video
const response = await fetch('http://localhost:5000/videos/generate', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({
    topic: 'The Future of AI',
    niche: 'Artificial Intelligence',
    language: 'English'
  })
});
const data = await response.json();
const videoId = data.video_id;

// Check status
const statusResponse = await fetch(`http://localhost:5000/videos/status/${videoId}`);
const status = await statusResponse.json();
console.log(status);
```

---

**Last Updated**: August 2024
