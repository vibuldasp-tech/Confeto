# 🐳 Docker - Quick Start

## 3-Step Deployment

### Step 1: Install Docker

```bash
# Install Docker
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh

# Add your user to docker group (no sudo needed)
sudo usermod -aG docker $USER
newgrp docker

# Install Docker Compose
sudo apt-get install docker-compose-plugin
```

### Step 2: Configure API Key

```bash
# Create .env file
cat > .env << EOF
OPENAI_API_KEY=sk-your-actual-key-here
AI_PROVIDER=openai
EOF
```

### Step 3: Start!

```bash
# Run automated setup
./docker-start.sh

# OR manually:
docker-compose up -d
```

**Done!** Visit: http://localhost:8000

---

## Quick Commands

```bash
# Start
docker-compose up -d

# Stop
docker-compose down

# View logs
docker-compose logs -f

# Restart
docker-compose restart

# Status
docker-compose ps

# Rebuild
docker-compose up -d --build
```

---

## 🎯 What You Get

- ✅ **Web application** running in container
- ✅ **Automatic restart** if container crashes
- ✅ **Health checks** built-in
- ✅ **Persistent storage** for uploads
- ✅ **Easy updates** with rebuild
- ✅ **Production ready** with Nginx option

---

## 🌐 Access Your App

- **Local:** http://localhost:8000
- **Network:** http://your-server-ip:8000
- **With domain:** http://your-domain.com (after DNS setup)

---

## 🔒 Production Setup (with SSL)

### 1. Get SSL Certificate

```bash
# Using Let's Encrypt
sudo certbot certonly --standalone -d your-domain.com

# Copy certificates
mkdir ssl
sudo cp /etc/letsencrypt/live/your-domain.com/fullchain.pem ssl/cert.pem
sudo cp /etc/letsencrypt/live/your-domain.com/privkey.pem ssl/key.pem
sudo chmod 644 ssl/*.pem
```

### 2. Start with Nginx

```bash
# Start with nginx reverse proxy + SSL
docker-compose --profile production up -d
```

**Access:** https://your-domain.com

---

## 📊 What's Running

### Containers:

1. **gap-analyzer-web** - Main web application
   - Port: 8000
   - Framework: Flask + Gunicorn
   - Workers: 2

2. **gap-analyzer-nginx** (optional, with `--profile production`)
   - Port: 80 (HTTP)
   - Port: 443 (HTTPS)
   - Features: SSL, rate limiting, caching

### Volumes:

- `web/uploads` - Mounted for file storage

---

## 🔧 Configuration

### Change Port

Edit `docker-compose.yml`:

```yaml
services:
  web:
    ports:
      - "3000:8000"  # External port 3000
```

### Increase Workers

Edit `docker-compose.yml`:

```yaml
services:
  web:
    command: gunicorn --chdir web --bind 0.0.0.0:8000 --workers 4 --timeout 120 app:app
```

### Add Memory Limits

```yaml
services:
  web:
    deploy:
      resources:
        limits:
          memory: 2G
```

---

## 🌍 Deploy to Cloud

### AWS EC2

```bash
# 1. Launch Ubuntu instance
# 2. SSH in
ssh -i key.pem ubuntu@your-ec2-ip

# 3. Install Docker (see Step 1 above)
# 4. Clone repo
git clone your-repo
cd document-gap-analyzer

# 5. Configure
nano .env  # Add API key

# 6. Deploy
docker-compose up -d

# 7. Access
# http://your-ec2-public-ip:8000
```

### DigitalOcean

```bash
# 1. Create Droplet (Ubuntu)
# 2. Same steps as AWS EC2
```

### Google Cloud

```bash
# Build and push
gcloud builds submit --tag gcr.io/YOUR_PROJECT/gap-analyzer

# Deploy to Cloud Run
gcloud run deploy gap-analyzer \
  --image gcr.io/YOUR_PROJECT/gap-analyzer \
  --platform managed \
  --allow-unauthenticated \
  --set-env-vars OPENAI_API_KEY=sk-your-key \
  --port 8000
```

---

## 🐛 Troubleshooting

### Check if running

```bash
docker-compose ps
```

Expected output:
```
NAME                   STATUS    PORTS
gap-analyzer-web       Up        0.0.0.0:8000->8000/tcp
```

### View logs

```bash
docker-compose logs -f web
```

### Test health endpoint

```bash
curl http://localhost:8000/health
```

Expected:
```json
{"status": "healthy", "timestamp": "..."}
```

### Restart container

```bash
docker-compose restart web
```

### Rebuild from scratch

```bash
docker-compose down
docker-compose build --no-cache
docker-compose up -d
```

---

## 📦 File Structure

```
/workspace/
├── Dockerfile              ← Container definition
├── docker-compose.yml      ← Orchestration config
├── .dockerignore          ← Files to ignore
├── nginx.conf             ← Nginx config (optional)
├── docker-start.sh        ← Quick start script
├── .env                   ← Your API key (create this)
└── web/
    ├── app.py            ← Flask application
    ├── templates/        ← HTML
    ├── static/           ← CSS/JS
    └── uploads/          ← File storage (mounted)
```

---

## 💰 Costs

### Self-Hosted (VPS + Docker)

- **Server:** $5-12/month (DigitalOcean, Linode, Vultr)
- **AI API:** $10-30/month (for 1000 analyses)
- **Total:** ~$15-42/month

### Cloud Platforms

- **Google Cloud Run:** $5-20/month (serverless)
- **AWS ECS:** $15-30/month
- **Azure Containers:** $20-40/month

---

## ✅ Complete Example

```bash
# 1. Install Docker
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh
sudo usermod -aG docker $USER
newgrp docker

# 2. Clone repo
git clone https://github.com/your-repo/document-gap-analyzer.git
cd document-gap-analyzer

# 3. Create .env
echo "OPENAI_API_KEY=sk-your-actual-key" > .env

# 4. Start
docker-compose up -d

# 5. Check
docker-compose logs -f

# 6. Visit
# http://localhost:8000
```

---

## 🎉 You're Running!

Your Docker deployment is complete!

**Next steps:**
- Upload documents and test
- Set up SSL for production
- Configure domain name
- Monitor logs
- Set up backups

**For full details:** See `DOCKER_GUIDE.md`

---

## 📞 Quick Reference

| Command | Purpose |
|---------|---------|
| `./docker-start.sh` | Quick automated setup |
| `docker-compose up -d` | Start containers |
| `docker-compose down` | Stop containers |
| `docker-compose logs -f` | View logs |
| `docker-compose ps` | Check status |
| `docker-compose restart` | Restart |
| `docker-compose up -d --build` | Rebuild |

---

**Happy Dockerizing! 🐳**
