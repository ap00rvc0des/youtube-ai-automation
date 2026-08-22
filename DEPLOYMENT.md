# 🐳 Docker & Deployment Guide

## Docker Setup

### Using Docker Compose (Recommended)

```bash
# Clone repository
git clone https://github.com/ap00rvc0des/youtube-ai-automation.git
cd youtube-ai-automation

# Copy environment file
cp .env.example .env

# Start all services
docker-compose up -d

# Check status
docker-compose ps

# View logs
docker-compose logs -f

# Stop services
docker-compose down

# Remove volumes (cleanup)
docker-compose down -v
```

### Accessing Services

- **Frontend**: http://localhost:3000
- **Backend API**: http://localhost:5000
- **Ollama**: http://localhost:11434
- **Piper TTS**: http://localhost:8000

## Docker Build

### Build Custom Image

```bash
# Build the Docker image
docker build -t youtube-ai-automation:latest .

# Run container
docker run -d \
  --name youtube-ai \
  -p 5000:5000 \
  -p 3000:3000 \
  -v $(pwd)/storage:/app/storage \
  -v $(pwd)/temp:/app/temp \
  youtube-ai-automation:latest

# View logs
docker logs -f youtube-ai

# Stop container
docker stop youtube-ai
docker rm youtube-ai
```

### Docker Hub

```bash
# Tag for Docker Hub
docker tag youtube-ai-automation:latest YOUR_USERNAME/youtube-ai-automation:latest

# Push to Docker Hub
docker push YOUR_USERNAME/youtube-ai-automation:latest

# Pull from Docker Hub
docker pull YOUR_USERNAME/youtube-ai-automation:latest
```

## Environment Setup

### Production .env

```bash
BACKEND_HOST=0.0.0.0
BACKEND_PORT=5000
FRONTEND_PORT=3000
ENVIRONMENT=production

OLLAMA_HOST=http://ollama:11434
OLLAMA_MODEL=neural-chat

PIPER_HOST=tts
PIPER_PORT=8000

STORAGE_PATH=/app/storage
TEMP_PATH=/app/temp

# YouTube OAuth (if needed)
YOUTUBE_CLIENT_ID=your_id
YOUTUBE_CLIENT_SECRET=your_secret

# Optional APIs
PEXELS_API_KEY=your_key
PIXABAY_API_KEY=your_key
```

## Cloud Deployment

### AWS EC2

```bash
# Launch EC2 instance (Ubuntu 22.04)
aws ec2 run-instances \
  --image-id ami-0c55b159cbfafe1f0 \
  --instance-type t3.large \
  --key-name my-key \
  --security-groups youtube-ai

# SSH into instance
ssh -i my-key.pem ubuntu@PUBLIC_IP

# Install Docker
sudo apt-get update
sudo apt-get install docker.io docker-compose
sudo usermod -aG docker ubuntu

# Clone and deploy
git clone https://github.com/ap00rvc0des/youtube-ai-automation.git
cd youtube-ai-automation
docker-compose up -d

# Access via public IP
http://PUBLIC_IP:3000
```

### Google Cloud Run

```bash
# Build and push image
gcloud builds submit --tag gcr.io/PROJECT_ID/youtube-ai

# Deploy
gcloud run deploy youtube-ai \
  --image gcr.io/PROJECT_ID/youtube-ai \
  --platform managed \
  --region us-central1 \
  --memory 4Gi
```

### Azure Container Instances

```bash
# Build image
docker build -t youtube-ai-automation .

# Push to Azure
az acr build --registry myregistry --image youtube-ai:latest .

# Deploy container
az container create \
  --resource-group mygroup \
  --name youtube-ai \
  --image myregistry.azurecr.io/youtube-ai:latest \
  --cpu 2 \
  --memory 4
```

### DigitalOcean

```bash
# Create droplet (Ubuntu 22.04, 4GB RAM)
doctl compute droplet create youtube-ai \
  --image ubuntu-22-04-x64 \
  --size s-2vcpu-4gb \
  --region nyc3

# SSH and setup
ssh root@DROPLET_IP

# Install dependencies
apt-get update && apt-get install -y docker.io docker-compose

# Deploy
git clone https://github.com/ap00rvc0des/youtube-ai-automation.git
cd youtube-ai-automation
docker-compose up -d
```

## Kubernetes Deployment

### Kubernetes YAML

```yaml
# deployment.yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: youtube-ai
spec:
  replicas: 1
  selector:
    matchLabels:
      app: youtube-ai
  template:
    metadata:
      labels:
        app: youtube-ai
    spec:
      containers:
      - name: youtube-ai
        image: youtube-ai-automation:latest
        ports:
        - containerPort: 5000
        - containerPort: 3000
        resources:
          requests:
            memory: "4Gi"
            cpu: "2000m"
          limits:
            memory: "8Gi"
            cpu: "4000m"
---
apiVersion: v1
kind: Service
metadata:
  name: youtube-ai-service
spec:
  selector:
    app: youtube-ai
  ports:
  - name: backend
    port: 5000
  - name: frontend
    port: 3000
  type: LoadBalancer
```

### Deploy to Kubernetes

```bash
# Create namespace
kubectl create namespace youtube-ai

# Deploy
kubectl apply -f deployment.yaml -n youtube-ai

# Check status
kubectl get pods -n youtube-ai
kubectl get svc -n youtube-ai

# View logs
kubectl logs -f deployment/youtube-ai -n youtube-ai
```

## Performance Optimization

### Resource Limits

```yaml
resources:
  requests:
    memory: "4Gi"
    cpu: "2"
  limits:
    memory: "8Gi"
    cpu: "4"
```

### Caching Strategy

```bash
# Redis for caching (in docker-compose.yml)
redis:
  image: redis:latest
  ports:
    - "6379:6379"
```

### Database Optimization

- Use PostgreSQL for production
- Index frequently queried columns
- Implement connection pooling

## Monitoring & Logging

### Prometheus

```yaml
services:
  prometheus:
    image: prom/prometheus:latest
    ports:
      - "9090:9090"
    volumes:
      - ./prometheus.yml:/etc/prometheus/prometheus.yml
```

### ELK Stack

```yaml
services:
  elasticsearch:
    image: docker.elastic.co/elasticsearch/elasticsearch:latest
    environment:
      - discovery.type=single-node
  kibana:
    image: docker.elastic.co/kibana/kibana:latest
    ports:
      - "5601:5601"
```

## Backup & Recovery

```bash
# Backup storage volumes
docker run --rm \
  -v youtube-ai_storage:/data \
  -v $(pwd)/backups:/backup \
  ubuntu tar czf /backup/storage.tar.gz -C /data .

# Restore from backup
docker run --rm \
  -v youtube-ai_storage:/data \
  -v $(pwd)/backups:/backup \
  ubuntu tar xzf /backup/storage.tar.gz -C /data
```

## SSL/TLS Setup

```bash
# Using Let's Encrypt with Certbot
sudo certbot certonly --standalone -d yourdomain.com

# Configure reverse proxy (Nginx)
server {
    listen 443 ssl;
    server_name yourdomain.com;
    
    ssl_certificate /etc/letsencrypt/live/yourdomain.com/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/yourdomain.com/privkey.pem;
    
    location / {
        proxy_pass http://localhost:3000;
    }
}
```

---

For production deployments, consult cloud provider documentation.
