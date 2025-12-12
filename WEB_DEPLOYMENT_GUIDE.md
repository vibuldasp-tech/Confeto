# 🌐 Web Deployment Guide

## Overview

This guide shows you how to host the Document Gap Analysis Tool as a **web application** where users can:
- Upload documents through a web interface
- Run gap analysis online
- Download reports in their browser
- No command-line needed!

---

## 🏗️ Architecture Options

### Option 1: Simple Web App (Recommended)
```
User Browser → Flask/FastAPI → Gap Analyzer → AI → Report
```
- Users upload files via web form
- Server processes and returns results
- Can be hosted on cloud platforms

### Option 2: Full SaaS Application
```
User → Web UI → API Gateway → Worker Queue → Database → S3 Storage
```
- Multiple users, authentication
- Job queue for processing
- Database for results
- Production-ready

We'll start with **Option 1** (simpler, faster to deploy).

---

## 📦 What We'll Build

### Web Interface Features:
1. **Upload Form** - Drag & drop PDF/Word files
2. **Progress Indicator** - See analysis progress
3. **Results Page** - View gap analysis results
4. **Download Reports** - Get Markdown, HTML, or JSON
5. **Responsive Design** - Works on mobile/desktop

### Technology Stack:
- **Backend**: Flask (Python web framework)
- **Frontend**: HTML/CSS/JavaScript
- **Hosting**: Multiple options (see below)

---

## 🚀 Quick Setup (Local Testing)

I'll create the web application files for you. Here's what you'll get:

```
web/
├── app.py              # Flask application
├── templates/          # HTML templates
│   ├── index.html     # Upload page
│   └── results.html   # Results page
├── static/            # CSS/JS files
│   ├── style.css
│   └── script.js
└── uploads/           # Temporary file storage
```

---

## 🔧 Deployment Options

### Option A: Heroku (Easiest, Free Tier Available)
- ✅ Easy deployment
- ✅ Free tier available
- ✅ Automatic SSL
- ⚠️ Cold starts on free tier

### Option B: Railway.app (Modern, Simple)
- ✅ Very easy deployment
- ✅ Free tier
- ✅ Fast
- ✅ GitHub integration

### Option C: AWS EC2 (Full Control)
- ✅ Complete control
- ✅ Scalable
- ⚠️ More complex setup
- 💰 Pay per usage

### Option D: Google Cloud Run (Serverless)
- ✅ Scales to zero
- ✅ Pay per use
- ✅ Container-based
- ⚠️ Requires Docker

### Option E: DigitalOcean App Platform (Balance)
- ✅ Easy deployment
- ✅ Good performance
- ✅ Predictable pricing
- 💰 Starts at $5/month

---

## 📝 Step-by-Step: Deploy to Heroku

### Prerequisites:
1. Heroku account (free): https://signup.heroku.com/
2. Git installed
3. Heroku CLI installed

### Steps:

**1. Install Heroku CLI**
```bash
# Mac
brew tap heroku/brew && brew install heroku

# Windows
# Download from: https://devcenter.heroku.com/articles/heroku-cli

# Linux
curl https://cli-assets.heroku.com/install.sh | sh
```

**2. Login to Heroku**
```bash
heroku login
```

**3. Create Heroku App**
```bash
cd /workspace
heroku create your-gap-analyzer-app
```

**4. Set Environment Variables**
```bash
heroku config:set OPENAI_API_KEY=sk-your-key-here
heroku config:set AI_PROVIDER=openai
```

**5. Deploy**
```bash
git add .
git commit -m "Deploy web application"
git push heroku main
```

**6. Open Your Web App**
```bash
heroku open
```

Your web app is now live at: `https://your-gap-analyzer-app.herokuapp.com`

---

## 📝 Step-by-Step: Deploy to Railway.app

### Steps:

**1. Sign up at Railway.app**
- Go to: https://railway.app/
- Sign up with GitHub

**2. Create New Project**
- Click "New Project"
- Select "Deploy from GitHub repo"
- Choose your repository

**3. Add Environment Variables**
- Go to project settings
- Add: `OPENAI_API_KEY`
- Add: `AI_PROVIDER=openai`

**4. Deploy**
- Railway auto-deploys on push
- Get your URL from dashboard

Done! Your app is live.

---

## 📝 Step-by-Step: Deploy to AWS EC2

### Steps:

**1. Launch EC2 Instance**
```bash
# Choose Ubuntu 22.04 LTS
# t2.micro (free tier eligible)
# Open ports: 22 (SSH), 80 (HTTP), 443 (HTTPS)
```

**2. SSH into Instance**
```bash
ssh -i your-key.pem ubuntu@your-ec2-ip
```

**3. Install Dependencies**
```bash
# Update system
sudo apt update && sudo apt upgrade -y

# Install Python and dependencies
sudo apt install python3-pip python3-venv nginx -y

# Clone your repository
git clone https://github.com/your-repo/document-gap-analyzer.git
cd document-gap-analyzer

# Create virtual environment
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
pip install gunicorn
```

**4. Configure Environment**
```bash
# Create .env file
cp .env.example .env
nano .env
# Add your API keys
```

**5. Set Up Gunicorn**
```bash
# Create systemd service
sudo nano /etc/systemd/system/gap-analyzer.service
```

Add:
```ini
[Unit]
Description=Gap Analyzer Web App
After=network.target

[Service]
User=ubuntu
WorkingDirectory=/home/ubuntu/document-gap-analyzer/web
Environment="PATH=/home/ubuntu/document-gap-analyzer/venv/bin"
ExecStart=/home/ubuntu/document-gap-analyzer/venv/bin/gunicorn -w 4 -b 127.0.0.1:8000 app:app

[Install]
WantedBy=multi-user.target
```

**6. Configure Nginx**
```bash
sudo nano /etc/nginx/sites-available/gap-analyzer
```

Add:
```nginx
server {
    listen 80;
    server_name your-domain.com;

    location / {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }

    client_max_body_size 20M;
}
```

**7. Enable and Start**
```bash
sudo ln -s /etc/nginx/sites-available/gap-analyzer /etc/nginx/sites-enabled/
sudo systemctl start gap-analyzer
sudo systemctl enable gap-analyzer
sudo systemctl restart nginx
```

**8. Set Up SSL (Optional but Recommended)**
```bash
sudo apt install certbot python3-certbot-nginx -y
sudo certbot --nginx -d your-domain.com
```

Your app is now live at: `https://your-domain.com`

---

## 📝 Step-by-Step: Deploy with Docker

### 1. Create Dockerfile
```bash
# Already created in web/ directory
cd web
docker build -t gap-analyzer-web .
```

### 2. Run Locally
```bash
docker run -p 8000:8000 \
  -e OPENAI_API_KEY=sk-your-key \
  gap-analyzer-web
```

### 3. Deploy to Google Cloud Run
```bash
# Build and push to Google Container Registry
gcloud builds submit --tag gcr.io/your-project/gap-analyzer

# Deploy to Cloud Run
gcloud run deploy gap-analyzer \
  --image gcr.io/your-project/gap-analyzer \
  --platform managed \
  --region us-central1 \
  --allow-unauthenticated \
  --set-env-vars OPENAI_API_KEY=sk-your-key
```

---

## 🔒 Security Considerations

### Important Security Measures:

**1. API Key Protection**
```python
# Never expose API keys in frontend
# Always use environment variables
# Rotate keys regularly
```

**2. File Upload Security**
```python
# Validate file types
# Limit file sizes (20MB max)
# Scan for malware
# Use temporary storage
# Delete files after processing
```

**3. Rate Limiting**
```python
# Limit requests per IP
# Prevent abuse
# Monitor usage
```

**4. Authentication (For Production)**
```python
# Add user authentication
# API key management
# Usage tracking
# Billing integration
```

**5. HTTPS/SSL**
```bash
# Always use HTTPS in production
# Use Let's Encrypt for free SSL
```

---

## 💰 Cost Estimates

### Hosting Costs:

**Heroku:**
- Free tier: $0/month (limited)
- Hobby: $7/month
- Professional: $25/month

**Railway.app:**
- Free tier: $0/month (limited)
- Pro: Pay per usage (~$5-20/month)

**AWS EC2:**
- t2.micro (free tier): $0/month (1 year)
- t2.small: ~$17/month
- t2.medium: ~$34/month

**DigitalOcean:**
- Basic Droplet: $6/month
- App Platform: $5/month

**Google Cloud Run:**
- Pay per use: ~$5-20/month
- Free tier: 2M requests/month

### AI API Costs:
- OpenAI GPT-4: ~$0.01-0.03 per analysis
- Anthropic Claude: ~$0.01-0.03 per analysis

**Monthly estimate for 1000 analyses:**
- Hosting: $5-25/month
- AI API: $10-30/month
- **Total: $15-55/month**

---

## 📊 Scaling Options

### Small Scale (1-100 users/day)
- Single Heroku dyno or Railway
- SQLite database
- Local file storage
- Cost: ~$7-15/month

### Medium Scale (100-1000 users/day)
- Multiple web workers
- PostgreSQL database
- S3 for file storage
- Redis for caching
- Cost: ~$50-100/month

### Large Scale (1000+ users/day)
- Load balancer
- Auto-scaling workers
- CDN for static files
- Background job queue
- Database replicas
- Cost: ~$200-500/month

---

## 🎨 Customization Options

### Branding:
- Change colors in `static/style.css`
- Add your logo
- Custom domain name
- White-label option

### Features to Add:
- User authentication
- API access
- Usage dashboard
- Team collaboration
- Document history
- Email reports
- Webhook notifications
- Batch processing

### Integration Options:
- Slack notifications
- Google Drive integration
- Dropbox integration
- Microsoft 365 integration
- Zapier/Make.com

---

## 🧪 Testing Your Web App

### Local Testing:
```bash
cd web
python app.py
# Visit: http://localhost:5000
```

### Upload Test:
1. Upload a PDF/Word file
2. Upload reference documents
3. Click "Analyze"
4. Wait for results
5. Download report

### Performance Testing:
```bash
# Test with multiple files
# Check response times
# Monitor memory usage
# Test error handling
```

---

## 📱 Mobile Responsiveness

The web interface is fully responsive:
- ✅ Works on iPhone/Android
- ✅ Tablet optimized
- ✅ Desktop experience
- ✅ Progressive Web App (PWA) ready

---

## 🔧 Maintenance

### Regular Tasks:
- Monitor error logs
- Update dependencies
- Rotate API keys
- Clean up old files
- Check disk space
- Monitor costs

### Monitoring Tools:
- Sentry (error tracking)
- Google Analytics (usage)
- UptimeRobot (availability)
- CloudWatch (AWS metrics)

---

## 📚 Additional Resources

### Tutorials:
- Flask deployment: https://flask.palletsprojects.com/deployment/
- Heroku Python: https://devcenter.heroku.com/articles/getting-started-with-python
- Railway.app docs: https://docs.railway.app/

### Tools:
- Heroku CLI: https://devcenter.heroku.com/articles/heroku-cli
- Docker: https://docs.docker.com/
- Nginx: https://nginx.org/en/docs/

---

## 🎯 Quick Start Summary

**Fastest Deployment (Railway.app):**
1. Push code to GitHub
2. Sign up at Railway.app
3. Connect GitHub repo
4. Add environment variables
5. Deploy!

**Most Popular (Heroku):**
1. Install Heroku CLI
2. `heroku create`
3. `heroku config:set OPENAI_API_KEY=...`
4. `git push heroku main`
5. `heroku open`

**Most Control (AWS EC2):**
1. Launch Ubuntu instance
2. Install dependencies
3. Configure Nginx + Gunicorn
4. Set up SSL
5. Monitor and scale

---

## ✅ Next Steps

1. **Review web application files** (in `web/` directory)
2. **Test locally** with `python web/app.py`
3. **Choose deployment platform** (Heroku, Railway, AWS, etc.)
4. **Set up domain name** (optional)
5. **Configure SSL certificate**
6. **Launch!**

---

## 🆘 Troubleshooting

**Problem: "Module not found"**
```bash
pip install -r requirements.txt
pip install flask gunicorn
```

**Problem: "Port already in use"**
```bash
# Change port in app.py
app.run(port=5001)
```

**Problem: "File upload fails"**
```bash
# Check file size limits
# Increase in app.py: app.config['MAX_CONTENT_LENGTH']
```

**Problem: "Slow analysis"**
```bash
# Use faster AI model
# Add caching
# Optimize worker configuration
```

---

For detailed implementation files, see the `web/` directory!
