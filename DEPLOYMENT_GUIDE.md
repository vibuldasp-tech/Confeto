# EQUIS SAR MVP - Deployment Guide

## ⚠️ CRITICAL SECURITY WARNING

**READ THIS BEFORE DEPLOYING TO THE INTERNET:**

This application has **NO AUTHENTICATION OR SECURITY**:
- ❌ No user login system
- ❌ No access control
- ❌ No encryption
- ❌ Public workspaces accessible to anyone with the link
- ❌ No protection against abuse or data breaches

**DO NOT DEPLOY THIS TO PRODUCTION WITH REAL DATA**

This is a development MVP only. If you deploy this to a public website:
- Anyone can upload files to your server
- Anyone can access any workspace if they know the UUID
- Files are stored in plain text
- No protection against malicious uploads
- No rate limiting or DDoS protection

**You have been warned.**

---

## 🚀 Deployment Options

Below are several options for hosting this application on the internet. Choose based on your needs and budget.

---

## Option 1: Heroku (Easiest, ~$7/month)

### Prerequisites
- Heroku account (free to sign up)
- Heroku CLI installed

### Steps

1. **Install Heroku CLI**
```bash
# Mac
brew tap heroku/brew && brew install heroku

# Ubuntu/Debian
curl https://cli-assets.heroku.com/install.sh | sh

# Windows
# Download from https://devcenter.heroku.com/articles/heroku-cli
```

2. **Login to Heroku**
```bash
heroku login
```

3. **Create Heroku App**
```bash
cd /workspace
heroku create your-app-name-here
```

4. **Add Buildpack**
```bash
heroku buildpacks:set heroku/nodejs
```

5. **Configure for Heroku**

Update `package.json` to specify Node version:
```json
{
  "engines": {
    "node": "18.x"
  }
}
```

6. **Create Procfile**
```bash
echo "web: node server.js" > Procfile
```

7. **Handle File Storage**

⚠️ **Important**: Heroku has ephemeral filesystem. Files uploaded will be deleted on restart.

For persistent storage, you need to add an external storage solution:
- AWS S3
- Cloudinary
- Google Cloud Storage

Or use a database-backed solution (see modifications below).

8. **Deploy**
```bash
git add .
git commit -m "Deploy to Heroku"
git push heroku main
```

9. **Open Your App**
```bash
heroku open
```

**Cost**: ~$7/month for Hobby dyno

---

## Option 2: DigitalOcean App Platform (~$5/month)

### Steps

1. **Push to GitHub**
```bash
# Create a new GitHub repository
# Then push your code
git remote add origin https://github.com/yourusername/equis-sar-mvp.git
git push -u origin main
```

2. **Deploy on DigitalOcean**
- Go to https://cloud.digitalocean.com/apps
- Click "Create App"
- Connect your GitHub repository
- Select the branch (main)
- Configure:
  - **Build Command**: `npm install`
  - **Run Command**: `node server.js`
  - **HTTP Port**: 3000
- Click "Next" and deploy

3. **Add Volume for Storage** (Optional, +$1/month)
- In app settings, add a volume
- Mount to `/workspace/uploads`
- This persists uploaded files

**Cost**: $5-6/month

---

## Option 3: Railway.app (Free tier available)

### Steps

1. **Push to GitHub** (if not already done)
```bash
git remote add origin https://github.com/yourusername/equis-sar-mvp.git
git push -u origin main
```

2. **Deploy on Railway**
- Go to https://railway.app
- Click "New Project"
- Select "Deploy from GitHub repo"
- Choose your repository
- Railway auto-detects Node.js and deploys
- It will automatically run `npm install` and start the server

3. **Configure**
- Railway automatically sets PORT environment variable
- Your app is live at: `your-app.up.railway.app`

**Cost**: Free tier (500 hours/month), paid starts at $5/month

---

## Option 4: Render.com (Free tier available)

### Steps

1. **Push to GitHub** (if not already done)

2. **Deploy on Render**
- Go to https://render.com
- Click "New +" → "Web Service"
- Connect your GitHub repository
- Configure:
  - **Name**: equis-sar-mvp
  - **Environment**: Node
  - **Build Command**: `npm install`
  - **Start Command**: `node server.js`
  - **Instance Type**: Free or Starter ($7/month)

3. **Add Persistent Disk** (Paid plans only)
- In service settings, add a disk
- Mount path: `/workspace/uploads`
- This keeps uploaded files persistent

**Cost**: Free tier (spins down after inactivity), paid $7/month for persistent storage

---

## Option 5: AWS EC2 (Full Control, ~$5-10/month)

### Steps

1. **Launch EC2 Instance**
- Go to AWS Console → EC2
- Launch instance (Ubuntu 22.04 LTS)
- t3.micro instance ($5/month with reserved)
- Configure security group: Allow port 80, 443, 22

2. **Connect to Instance**
```bash
ssh -i your-key.pem ubuntu@your-ec2-ip
```

3. **Install Node.js**
```bash
curl -fsSL https://deb.nodesource.com/setup_18.x | sudo -E bash -
sudo apt-get install -y nodejs
sudo npm install -g pm2
```

4. **Deploy Your Code**
```bash
# Clone from GitHub
git clone https://github.com/yourusername/equis-sar-mvp.git
cd equis-sar-mvp
npm install
```

5. **Setup PM2 (Process Manager)**
```bash
pm2 start server.js --name equis-sar
pm2 startup
pm2 save
```

6. **Setup Nginx Reverse Proxy**
```bash
sudo apt install nginx
sudo nano /etc/nginx/sites-available/equis-sar
```

Add this configuration:
```nginx
server {
    listen 80;
    server_name your-domain.com;

    location / {
        proxy_pass http://localhost:3000;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection 'upgrade';
        proxy_set_header Host $host;
        proxy_cache_bypass $http_upgrade;
    }
}
```

```bash
sudo ln -s /etc/nginx/sites-available/equis-sar /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl restart nginx
```

7. **Setup Domain** (Optional but recommended)
- Buy a domain from Namecheap, GoDaddy, etc. (~$10-15/year)
- Point A record to your EC2 IP
- Setup SSL with Let's Encrypt:
```bash
sudo apt install certbot python3-certbot-nginx
sudo certbot --nginx -d your-domain.com
```

**Cost**: ~$5/month + domain (~$10-15/year)

---

## Option 6: VPS (Linode, Vultr, etc.) (~$5/month)

Similar to AWS EC2 but simpler:

1. **Create VPS**
- Linode: https://linode.com ($5/month for 1GB RAM)
- Vultr: https://vultr.com ($5/month)
- DigitalOcean Droplet: ($6/month)

2. **Follow AWS EC2 steps above** (same process)

**Cost**: $5-6/month + optional domain

---

## 🔧 Required Code Changes for Production

### 1. Update server.js for Production

Add at the top of `server.js`:

```javascript
// Production environment check
const isProduction = process.env.NODE_ENV === 'production';
const PORT = process.env.PORT || 3000;

// Add security headers (basic)
app.use((req, res, next) => {
  res.setHeader('X-Content-Type-Options', 'nosniff');
  res.setHeader('X-Frame-Options', 'DENY');
  res.setHeader('X-XSS-Protection', '1; mode=block');
  next();
});

// Add request logging in production
if (isProduction) {
  const morgan = require('morgan');
  app.use(morgan('combined'));
}
```

### 2. Add File Size Limits

Update multer configuration:

```javascript
const upload = multer({
  storage: storage,
  limits: {
    fileSize: 10 * 1024 * 1024 // 10MB limit
  },
  fileFilter: (req, file, cb) => {
    const ext = path.extname(file.originalname).toLowerCase();
    if (ext === '.docx' || ext === '.doc') {
      cb(null, true);
    } else {
      cb(new Error('Only .docx and .doc files are allowed'));
    }
  }
});
```

### 3. Add Environment Variables

Create `.env` file (don't commit to git):
```env
NODE_ENV=production
PORT=3000
MAX_FILE_SIZE=10485760
```

Install dotenv:
```bash
npm install dotenv
```

Add to top of `server.js`:
```javascript
require('dotenv').config();
```

### 4. Setup Database (Recommended)

For production, replace JSON files with a database:

**Option A: MongoDB Atlas (Free tier)**
```bash
npm install mongoose
```

**Option B: PostgreSQL**
```bash
npm install pg
```

**Option C: SQLite** (simplest, file-based)
```bash
npm install sqlite3
```

### 5. Add Rate Limiting

```bash
npm install express-rate-limit
```

Add to `server.js`:
```javascript
const rateLimit = require('express-rate-limit');

const uploadLimiter = rateLimit({
  windowMs: 15 * 60 * 1000, // 15 minutes
  max: 5 // limit each IP to 5 uploads per windowMs
});

app.post('/api/upload', uploadLimiter, upload.single('document'), async (req, res) => {
  // ... existing code
});
```

---

## 📋 Pre-Deployment Checklist

Before deploying to production:

- [ ] Add file size limits
- [ ] Add rate limiting
- [ ] Setup error logging
- [ ] Configure CORS if needed
- [ ] Setup monitoring (e.g., Sentry)
- [ ] Add health check endpoint
- [ ] Setup SSL/HTTPS
- [ ] Configure firewall rules
- [ ] Add backup system
- [ ] Test with various file types
- [ ] Load test the application
- [ ] Setup automated backups
- [ ] Add terms of service
- [ ] Add privacy policy
- [ ] Setup analytics (optional)
- [ ] Configure CDN for static files (optional)

---

## 💰 Cost Comparison

| Platform | Free Tier | Paid Tier | Best For |
|----------|-----------|-----------|----------|
| **Railway** | 500 hrs/mo | $5/mo | Quick MVP testing |
| **Render** | Yes (sleeps) | $7/mo | Simple deployment |
| **DigitalOcean** | No | $5/mo | App Platform ease |
| **Heroku** | No* | $7/mo | Mature ecosystem |
| **Linode VPS** | No | $5/mo | Full control |
| **AWS EC2** | 12mo free | $5-10/mo | Scalability |

*Heroku removed free tier in 2022

---

## 🔐 Security Enhancements for Production

**CRITICAL**: Before deploying with real data, you MUST add:

1. **Authentication System**
   - User registration/login
   - Session management
   - Password hashing (bcrypt)

2. **Authorization**
   - Workspace ownership
   - Access control lists
   - Private/public workspace settings

3. **Data Protection**
   - Encrypt files at rest
   - HTTPS/SSL (mandatory)
   - Secure headers

4. **Input Validation**
   - Sanitize all user inputs
   - Validate file contents
   - Check for malware

5. **Monitoring**
   - Error tracking (Sentry, Rollbar)
   - Performance monitoring
   - Security alerts

---

## 🚀 Quick Deploy (Railway - Fastest)

For the absolute fastest deployment:

```bash
# 1. Install Railway CLI
npm install -g @railway/cli

# 2. Login
railway login

# 3. Initialize
cd /workspace
railway init

# 4. Deploy
railway up

# 5. Get URL
railway domain
```

**Your app will be live in ~2 minutes!**

---

## 📞 Support & Resources

- **Heroku Docs**: https://devcenter.heroku.com/
- **Railway Docs**: https://docs.railway.app/
- **Render Docs**: https://render.com/docs
- **DigitalOcean Tutorials**: https://www.digitalocean.com/community/tutorials
- **AWS EC2 Guide**: https://docs.aws.amazon.com/ec2/

---

## ⚠️ Final Warning

**This application is NOT production-ready for sensitive data.**

Before deploying with real SAR documents or PII:
1. Hire a security professional
2. Implement authentication
3. Add encryption
4. Undergo security audit
5. Ensure HIPAA/SOC2/compliance if required

**You are responsible for any data breaches or security incidents.**

---

## ✅ Recommended Path

For your use case, I recommend:

1. **Testing/Demo**: Use **Railway** (free tier, 2 minutes to deploy)
2. **Production**: Use **AWS EC2** or **DigitalOcean Droplet** with:
   - Authentication added
   - Database instead of JSON files
   - SSL certificate
   - Regular backups
   - Security monitoring

---

Need help with deployment? Check the platform-specific documentation or reach out to their support teams.
