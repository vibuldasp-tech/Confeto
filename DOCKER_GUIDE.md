# 🐳 Docker Deployment Guide

Complete guide for deploying the Document Gap Analysis Tool using Docker.

---

## 📦 What's Included

- ✅ **Dockerfile** - Container definition
- ✅ **docker-compose.yml** - Easy orchestration
- ✅ **nginx.conf** - Production-ready reverse proxy
- ✅ **Health checks** - Automatic container monitoring
- ✅ **Volume mounts** - Persistent file storage
- ✅ **Environment variables** - Easy configuration

---

## 🚀 Quick Start (3 Steps)

### Step 1: Set Environment Variables

```bash
# Create .env file
cat > .env << EOF
OPENAI_API_KEY=sk-your-actual-key-here
AI_PROVIDER=openai
EOF
```

### Step 2: Build and Run

```bash
# Build and start the container
docker-compose up -d
```

### Step 3: Access Your App

Visit: **http://localhost:8000**

**That's it!** Your web application is running.

---

## 🔧 Docker Commands

### Start the Application

```bash
# Build and start in background
docker-compose up -d

# View logs
docker-compose logs -f

# Check status
docker-compose ps
```

### Stop the Application

```bash
# Stop containers
docker-compose down

# Stop and remove volumes
docker-compose down -v
```

### Rebuild After Changes

```bash
# Rebuild and restart
docker-compose up -d --build
```

### View Logs

```bash
# All logs
docker-compose logs -f

# Last 100 lines
docker-compose logs --tail=100

# Web service only
docker-compose logs -f web
```

---

## 🌐 Deployment Options

### Option 1: Simple Web App (Default)

**Best for:** Testing, small deployments

```bash
# Start web app only
docker-compose up -d web
```

**Access:** http://localhost:8000

### Option 2: With Nginx (Production)

**Best for:** Production, SSL, rate limiting

```bash
# Start with nginx reverse proxy
docker-compose --profile production up -d
```

**Access:** http://localhost (port 80)

### Option 3: Custom Port

```bash
# Change port in docker-compose.yml
ports:
  - "3000:8000"  # External:Internal

# Or use environment variable
PORT=3000 docker-compose up -d
```

---

## 🎯 Configuration

### Environment Variables

Edit `.env` file:

```bash
# Required: AI Provider API Key
OPENAI_API_KEY=sk-your-openai-key
# OR
ANTHROPIC_API_KEY=sk-ant-your-anthropic-key

# Optional: Choose provider
AI_PROVIDER=openai  # or 'anthropic'

# Optional: Change port
PORT=8000
```

### File Upload Limits

Edit `Dockerfile` or `docker-compose.yml`:

```yaml
environment:
  - MAX_CONTENT_LENGTH=20971520  # 20MB in bytes
```

---

## 🏭 Production Deployment

### With Nginx + SSL

**1. Get SSL Certificate**

```bash
# Create ssl directory
mkdir ssl

# Copy your certificates
cp cert.pem ssl/
cp key.pem ssl/

# Or use Let's Encrypt (see below)
```

**2. Edit nginx.conf**

Uncomment the HTTPS server block and update domain:

```nginx
server {
    listen 443 ssl http2;
    server_name your-domain.com;
    
    ssl_certificate /etc/nginx/ssl/cert.pem;
    ssl_certificate_key /etc/nginx/ssl/key.pem;
    ...
}
```

**3. Start with Nginx**

```bash
docker-compose --profile production up -d
```

**Access:** https://your-domain.com

---

## 🔒 SSL/HTTPS Setup

### Option A: Let's Encrypt (Free)

**1. Install Certbot**

```bash
# On host machine
sudo apt-get install certbot
```

**2. Get Certificate**

```bash
sudo certbot certonly --standalone -d your-domain.com
```

**3. Copy Certificates**

```bash
mkdir ssl
sudo cp /etc/letsencrypt/live/your-domain.com/fullchain.pem ssl/cert.pem
sudo cp /etc/letsencrypt/live/your-domain.com/privkey.pem ssl/key.pem
sudo chmod 644 ssl/*.pem
```

**4. Auto-Renewal**

```bash
# Add to crontab
0 0 1 * * certbot renew && docker-compose restart nginx
```

### Option B: Custom SSL Certificate

```bash
# Place your certificates in ssl/ directory
ssl/
├── cert.pem
└── key.pem
```

---

## 🌍 Cloud Deployment

### AWS EC2

**1. Launch EC2 Instance**
- Ubuntu 22.04 LTS
- t2.micro or larger
- Open ports: 22, 80, 443

**2. Install Docker**

```bash
ssh -i key.pem ubuntu@your-ec2-ip

# Update system
sudo apt-get update

# Install Docker
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh
sudo usermod -aG docker ubuntu

# Install Docker Compose
sudo apt-get install docker-compose-plugin
```

**3. Clone and Deploy**

```bash
# Clone repository
git clone https://github.com/your-repo/document-gap-analyzer.git
cd document-gap-analyzer

# Create .env
nano .env
# Add: OPENAI_API_KEY=sk-your-key

# Deploy
docker-compose up -d
```

**4. Configure Domain**

Point your domain DNS to EC2 public IP, then set up SSL.

### Google Cloud Run

**1. Build and Push Image**

```bash
# Set project
gcloud config set project YOUR_PROJECT_ID

# Build image
gcloud builds submit --tag gcr.io/YOUR_PROJECT_ID/gap-analyzer

# Deploy
gcloud run deploy gap-analyzer \
  --image gcr.io/YOUR_PROJECT_ID/gap-analyzer \
  --platform managed \
  --region us-central1 \
  --allow-unauthenticated \
  --set-env-vars OPENAI_API_KEY=sk-your-key \
  --port 8000 \
  --memory 2Gi \
  --timeout 120s
```

**2. Get URL**

```bash
gcloud run services describe gap-analyzer --region us-central1
```

### DigitalOcean

**1. Create Droplet**
- Ubuntu 22.04
- $6/month or higher
- Add SSH key

**2. Install Docker**

```bash
ssh root@your-droplet-ip

# Install Docker
curl -fsSL https://get.docker.com -o get-docker.sh
sh get-docker.sh

# Install Docker Compose
apt-get install docker-compose-plugin
```

**3. Deploy**

```bash
git clone your-repo
cd document-gap-analyzer
nano .env  # Add API key
docker-compose up -d
```

### Azure Container Instances

```bash
# Create resource group
az group create --name gap-analyzer-rg --location eastus

# Create container
az container create \
  --resource-group gap-analyzer-rg \
  --name gap-analyzer \
  --image your-registry/gap-analyzer:latest \
  --dns-name-label gap-analyzer-unique \
  --ports 8000 \
  --environment-variables \
    OPENAI_API_KEY=sk-your-key \
    AI_PROVIDER=openai
```

---

## 📊 Monitoring

### Health Check

```bash
# Check container health
docker-compose ps

# Manual health check
curl http://localhost:8000/health
```

Expected response:
```json
{
  "status": "healthy",
  "timestamp": "2024-12-12T10:00:00"
}
```

### View Logs

```bash
# Real-time logs
docker-compose logs -f

# Last 100 lines
docker-compose logs --tail=100 web

# Error logs only
docker-compose logs web | grep ERROR
```

### Resource Usage

```bash
# Container stats
docker stats

# Detailed info
docker-compose top
```

---

## 🔧 Troubleshooting

### Container Won't Start

```bash
# Check logs
docker-compose logs web

# Check configuration
docker-compose config

# Rebuild
docker-compose up -d --build --force-recreate
```

### "Module not found" Error

```bash
# Rebuild image
docker-compose build --no-cache web
docker-compose up -d
```

### "API key not configured"

```bash
# Check environment variables
docker-compose exec web env | grep API_KEY

# Update .env file
nano .env
docker-compose up -d
```

### Port Already in Use

```bash
# Change port in docker-compose.yml
ports:
  - "8001:8000"  # Use port 8001 instead

# Or stop conflicting service
sudo lsof -i :8000
sudo kill -9 <PID>
```

### File Upload Fails

```bash
# Check uploads directory permissions
docker-compose exec web ls -la web/uploads

# Fix permissions
docker-compose exec web chmod 777 web/uploads
```

### Slow Performance

```bash
# Increase workers in docker-compose.yml
command: gunicorn --chdir web --bind 0.0.0.0:8000 --workers 4 --timeout 120 app:app

# Restart
docker-compose up -d
```

---

## 🎛️ Advanced Configuration

### Multiple Workers

```yaml
# docker-compose.yml
services:
  web:
    command: gunicorn --chdir web --bind 0.0.0.0:8000 --workers 4 --timeout 120 app:app
```

### Custom Memory Limits

```yaml
services:
  web:
    deploy:
      resources:
        limits:
          memory: 2G
        reservations:
          memory: 1G
```

### Auto-Restart

```yaml
services:
  web:
    restart: unless-stopped
```

### Background Jobs (Future)

```yaml
services:
  web:
    ...
  
  worker:
    build: .
    command: celery -A app.celery worker
    environment:
      - CELERY_BROKER_URL=redis://redis:6379/0
  
  redis:
    image: redis:alpine
```

---

## 📦 Pre-Built Images

### Option A: Use Docker Hub (Coming Soon)

```bash
# Pull pre-built image
docker pull yourusername/gap-analyzer:latest

# Run
docker run -p 8000:8000 \
  -e OPENAI_API_KEY=sk-your-key \
  yourusername/gap-analyzer:latest
```

### Option B: Build Locally

```bash
# Build image
docker build -t gap-analyzer .

# Run
docker run -p 8000:8000 \
  -e OPENAI_API_KEY=sk-your-key \
  gap-analyzer
```

---

## 🔄 Updates and Maintenance

### Update Application

```bash
# Pull latest code
git pull

# Rebuild and restart
docker-compose up -d --build

# Clean old images
docker image prune -a
```

### Backup Data

```bash
# Backup uploads directory
docker-compose exec web tar -czf /tmp/uploads-backup.tar.gz web/uploads
docker cp gap-analyzer-web:/tmp/uploads-backup.tar.gz ./backups/

# Or use volume backup
docker run --rm \
  -v gap-analyzer_uploads:/data \
  -v $(pwd)/backups:/backup \
  alpine tar -czf /backup/uploads-backup.tar.gz /data
```

### Database (Future)

```yaml
# Add PostgreSQL
services:
  db:
    image: postgres:15
    environment:
      POSTGRES_PASSWORD: your_password
    volumes:
      - postgres_data:/var/lib/postgresql/data

volumes:
  postgres_data:
```

---

## 💰 Cost Estimates

### Self-Hosted (Docker on VPS)

| Provider | Size | Cost/Month |
|----------|------|------------|
| DigitalOcean | 2GB RAM | $12 |
| Linode | 2GB RAM | $12 |
| Vultr | 2GB RAM | $12 |
| AWS EC2 | t2.small | ~$17 |
| Hetzner | 2GB RAM | €4.50 (~$5) |

### Cloud Platforms

| Platform | Cost | Notes |
|----------|------|-------|
| Google Cloud Run | $5-20/month | Pay per use |
| AWS ECS | $15-30/month | Container service |
| Azure Container | $20-40/month | Container instances |

**Plus AI API costs:** ~$10-30/month for 1000 analyses

---

## 📋 Complete Example

### Deploy on Ubuntu Server

```bash
# 1. Install Docker
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh
sudo usermod -aG docker $USER
newgrp docker

# 2. Clone repository
git clone https://github.com/your-repo/document-gap-analyzer.git
cd document-gap-analyzer

# 3. Configure
cat > .env << EOF
OPENAI_API_KEY=sk-your-actual-key-here
AI_PROVIDER=openai
EOF

# 4. Start
docker-compose up -d

# 5. Check
docker-compose ps
curl http://localhost:8000/health

# 6. View logs
docker-compose logs -f

# 7. Access
# Visit: http://your-server-ip:8000
```

**Done!** Your application is running.

---

## ✅ Pre-Flight Checklist

Before deploying:

- [ ] Docker installed
- [ ] Docker Compose installed
- [ ] `.env` file created with API key
- [ ] Ports 8000 (or 80/443) available
- [ ] Sufficient disk space (5GB+)
- [ ] Sufficient RAM (2GB+ recommended)
- [ ] Domain pointed to server (if using SSL)
- [ ] SSL certificates ready (if using HTTPS)

---

## 🎉 You're Ready!

Your Docker deployment is configured and ready to go.

**Quick Start:**
```bash
# Create .env
echo "OPENAI_API_KEY=sk-your-key" > .env

# Start
docker-compose up -d

# Visit
# http://localhost:8000
```

**Production with SSL:**
```bash
# Setup SSL certificates
mkdir ssl
# Add cert.pem and key.pem

# Start with nginx
docker-compose --profile production up -d

# Visit
# https://your-domain.com
```

Happy Dockerizing! 🐳
