# 🚀 Deploy EQUIS SAR MVP to the Internet (Quick Guide)

## ⚠️ SECURITY WARNING
This app has **NO AUTHENTICATION**. Anyone can upload files and access workspaces. **Not safe for real data!**

---

## 🎯 Fastest Option: Railway (2 minutes, FREE)

### Method 1: One-Click Deploy (Easiest)

1. **Push to GitHub**
   - Create a new repository on GitHub
   - Push this code:
   ```bash
   cd /workspace
   git init
   git add .
   git commit -m "Initial commit"
   git remote add origin https://github.com/YOUR_USERNAME/equis-sar-mvp.git
   git push -u origin main
   ```

2. **Deploy on Railway**
   - Go to: https://railway.app
   - Click "Start a New Project"
   - Select "Deploy from GitHub repo"
   - Choose your repository
   - Railway auto-deploys!
   - Get your URL: `https://your-app.up.railway.app`

**Done! Your app is live in ~2 minutes!** ✅

---

### Method 2: Railway CLI

```bash
# Install Railway CLI
npm install -g @railway/cli

# Login
railway login

# Deploy
cd /workspace
railway init
railway up

# Get your URL
railway domain
```

**Your app is live!** 🎉

---

## 💰 Free Tier Limits

Railway Free Tier:
- ✅ 500 hours/month (~20 days)
- ✅ $5 credit included
- ✅ Custom domain support
- ⚠️ Uploads deleted on restart (ephemeral storage)

**Note**: Uploaded files will be lost when the app restarts. For persistent storage, upgrade to paid plan ($5/mo).

---

## 🔗 Other Quick Options

### Option 2: Render.com (Free, but sleeps)
1. Go to https://render.com
2. New → Web Service
3. Connect GitHub repo
4. Auto-deploys!
- ⚠️ Spins down after 15 min inactivity (free tier)

### Option 3: Heroku (~$7/month)
```bash
# Install Heroku CLI
brew install heroku/brew/heroku  # Mac
# or download from heroku.com

# Deploy
heroku login
heroku create your-app-name
git push heroku main
heroku open
```

---

## 📋 What You Need

### Required:
- [ ] GitHub account (free)
- [ ] Railway/Render/Heroku account (free)

### Optional:
- [ ] Custom domain (~$10/year from Namecheap, GoDaddy)
- [ ] Paid plan for persistent storage (~$5/month)

---

## 🔧 After Deployment

Your app will be live at a URL like:
- Railway: `https://equis-sar-mvp.up.railway.app`
- Render: `https://equis-sar-mvp.onrender.com`
- Heroku: `https://your-app-name.herokuapp.com`

### Test Your Deployed App:
1. Visit your app URL
2. Upload `Test_SAR_Document.docx`
3. Verify sections are detected
4. Edit and save a section
5. ⚠️ Note: Files may be lost on restart (free tiers)

---

## ⚙️ Custom Domain (Optional)

### With Railway:
1. Buy domain from Namecheap/GoDaddy (~$10/year)
2. Railway dashboard → Settings → Domains
3. Add custom domain
4. Update DNS records (Railway provides instructions)
5. SSL automatically configured!

---

## 🛡️ Making It Production-Ready

**This MVP is NOT production-ready!** To use with real data:

### Must Add:
1. **Authentication** - User login system
2. **Database** - Replace JSON files with PostgreSQL/MongoDB
3. **Encryption** - Encrypt stored files
4. **Rate Limiting** - Prevent abuse
5. **File Validation** - Scan for viruses
6. **Backup System** - Automated backups

### Estimated Cost for Production:
- **Railway Pro**: $5/month (persistent storage)
- **Database** (Railway): $5/month
- **Custom Domain**: $10-15/year
- **Total**: ~$10-15/month

---

## 📊 Deployment Comparison

| Platform | Deploy Time | Free Tier | Persistent Files | Custom Domain |
|----------|-------------|-----------|------------------|---------------|
| **Railway** | 2 min | 500 hrs/mo | Paid only | ✅ |
| **Render** | 3 min | Yes* | Paid only | ✅ |
| **Heroku** | 5 min | No | Paid only | ✅ |

*Render free tier sleeps after 15 min inactivity

---

## 🎬 Step-by-Step Video Guides

- **Railway**: https://docs.railway.app/deploy/deployments
- **Render**: https://render.com/docs/deploy-node-express-app
- **Heroku**: https://devcenter.heroku.com/articles/deploying-nodejs

---

## ❓ Troubleshooting

### "Application Error" after deploy
- Check logs: `railway logs` or Render/Heroku dashboard
- Verify `package.json` has correct start script
- Ensure Node version specified in `package.json`

### "Workspace not found" after upload
- Free tier has ephemeral storage
- Files deleted on restart
- Solution: Upgrade to paid plan with persistent disk

### Upload fails
- Check file size limit
- Verify .docx file format
- Check deployment logs

---

## ✅ Recommended: Railway for Testing

**Best for this MVP:**
1. **Quick testing**: Railway (free, 2 minutes)
2. **Demo/prototype**: Railway Pro ($5/mo)
3. **Production**: Need to add auth + database first

---

## 🚨 Security Reminder

**Before sharing your deployed URL:**
- ⚠️ Anyone can upload files to your server
- ⚠️ Anyone can access any workspace
- ⚠️ No protection against malicious uploads
- ⚠️ Not HIPAA or SOC2 compliant

**Only use for testing with non-sensitive data!**

---

## 🎉 Quick Start (Copy-Paste)

```bash
# 1. Push to GitHub (replace YOUR_USERNAME)
cd /workspace
git init
git add .
git commit -m "Deploy EQUIS SAR MVP"
git branch -M main
git remote add origin https://github.com/YOUR_USERNAME/equis-sar-mvp.git
git push -u origin main

# 2. Install Railway CLI
npm install -g @railway/cli

# 3. Deploy
railway login
railway init
railway up

# 4. Get URL
railway domain

# Done! 🎉
```

---

Your app is now live on the internet! 🌍

For full deployment details, see `DEPLOYMENT_GUIDE.md`.
