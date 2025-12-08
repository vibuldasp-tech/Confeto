# Deploy EQUIS SAR MVP to Render - Step by Step

## 🚀 Render Deployment Guide

Follow these steps to deploy your application to Render.

---

## Step 1: Push Code to GitHub

### If you haven't already:

```bash
cd /workspace

# Initialize git (if not already done)
git init

# Add all files
git add .

# Commit
git commit -m "Deploy EQUIS SAR MVP to Render"

# Create main branch
git branch -M main
```

### Push to GitHub:

1. **Go to GitHub.com and create a new repository:**
   - Repository name: `equis-sar-mvp`
   - Description: "EQUIS SAR MVP - Document analysis workspace"
   - Privacy: Public or Private (your choice)
   - **Don't** add README, .gitignore, or license (we already have them)
   - Click "Create repository"

2. **Push your code:**
   ```bash
   # Replace YOUR_USERNAME with your GitHub username
   git remote add origin https://github.com/YOUR_USERNAME/equis-sar-mvp.git
   git push -u origin main
   ```

---

## Step 2: Create Render Account

1. Go to: **https://render.com**
2. Click **"Get Started"** or **"Sign Up"**
3. Sign up with:
   - GitHub account (recommended - easiest)
   - Or email/password
4. Verify your email if needed

---

## Step 3: Deploy Web Service

### 3a. Connect GitHub Repository

1. **Dashboard:** Click **"New +"** button (top right)
2. Select: **"Web Service"**
3. **Connect GitHub:**
   - If first time: Click "Connect GitHub"
   - Authorize Render to access your repositories
   - Select your `equis-sar-mvp` repository
4. Click **"Connect"** next to your repository

### 3b. Configure Your Service

Fill in these settings:

**Basic Settings:**
- **Name:** `equis-sar-mvp` (or your preferred name)
- **Region:** Choose closest to your users (e.g., Oregon, Ohio, Frankfurt)
- **Branch:** `main`
- **Root Directory:** Leave blank
- **Environment:** `Node`

**Build & Deploy:**
- **Build Command:** `npm install`
- **Start Command:** `node server.js`

**Instance Type:**
- **Free** (for testing - sleeps after 15 min inactivity)
- **Starter** ($7/month - always on, better for demos)

**Advanced (Optional):**
- **Auto-Deploy:** Yes (recommended - deploys automatically on git push)

### 3c. Create Web Service

1. Click **"Create Web Service"** at the bottom
2. Wait for deployment (usually 2-5 minutes)
3. Watch the logs as it builds

You'll see:
```
==> Downloading Node...
==> Installing dependencies...
==> Build successful
==> Starting service...
EQUIS SAR MVP server running on http://localhost:10000
```

---

## Step 4: Access Your App

Once deployed:

1. **Your URL:** `https://equis-sar-mvp-xxxx.onrender.com`
   - Find it at the top of your service page
2. **Click the URL** to open your app
3. **Test it:**
   - Upload `Test_SAR_Document.docx`
   - Create a workspace
   - Edit sections

---

## ⚠️ Important: File Storage on Free Tier

### Free Tier Limitation:
- **Ephemeral storage:** Uploaded files are deleted when app restarts/redeploys
- **Sleeps after 15 min:** App spins down after inactivity, loses uploaded files

### Solutions:

#### Option 1: Upgrade to Starter Plan ($7/month)
- Always on (no sleeping)
- Still ephemeral storage BUT less frequent restarts
- **Still need persistent disk** (see Option 2)

#### Option 2: Add Persistent Disk ($1-5/month)
Only available on paid plans:
1. Go to your service dashboard
2. Click **"Disks"** in left menu
3. Click **"Add Disk"**
4. Configure:
   - **Name:** `uploads-storage`
   - **Mount Path:** `/workspace/uploads`
   - **Size:** 1 GB (enough for testing)
5. Click **"Create Disk"**
6. Service will redeploy automatically

**Cost:** Starter ($7/mo) + Disk ($1/GB/mo) = ~$8/month total

#### Option 3: Use Database (Better for Production)
Replace JSON files with database:
- PostgreSQL (Render provides free tier)
- See DEPLOYMENT_GUIDE.md for implementation

---

## Step 5: Custom Domain (Optional)

### With Free/Starter Plan:

1. **Buy a domain:**
   - Namecheap.com (~$10/year)
   - GoDaddy.com (~$12/year)
   - Google Domains (~$12/year)

2. **Add to Render:**
   - Service dashboard → **"Settings"** → **"Custom Domains"**
   - Click **"Add Custom Domain"**
   - Enter: `your-domain.com` or `app.your-domain.com`
   - Render shows DNS records to add

3. **Update DNS:**
   - Go to your domain registrar
   - Add DNS records shown by Render
   - Usually: CNAME or A record

4. **Wait for SSL:**
   - Render automatically provisions SSL certificate
   - Takes 5-60 minutes
   - Your app will be at `https://your-domain.com`

---

## 📊 Monitoring Your App

### View Logs:
1. Service dashboard → **"Logs"** tab
2. See real-time application logs
3. Filter by severity (Info, Warning, Error)

### Metrics:
1. Service dashboard → **"Metrics"** tab
2. View:
   - CPU usage
   - Memory usage
   - Request count
   - Response time

### Check Health:
- Look for: "EQUIS SAR MVP server running on..."
- If errors, check logs

---

## 🔄 Making Updates

### Automatic Deploys (Recommended):

```bash
# Make changes to code
nano server.js

# Commit and push
git add .
git commit -m "Update feature"
git push origin main

# Render automatically detects and redeploys!
```

### Manual Deploy:
1. Go to service dashboard
2. Click **"Manual Deploy"** → **"Deploy latest commit"**

---

## ⚙️ Environment Variables (Optional)

Add environment variables for configuration:

1. Service dashboard → **"Environment"** tab
2. Click **"Add Environment Variable"**
3. Add:
   - **Key:** `NODE_ENV` **Value:** `production`
   - **Key:** `MAX_FILE_SIZE` **Value:** `10485760`

4. Click **"Save Changes"**
5. Service redeploys automatically

---

## 🛑 Troubleshooting

### Issue: "Application failed to respond"
**Solution:**
- Check logs for errors
- Verify `package.json` has correct start script
- Ensure port is from `process.env.PORT`

### Issue: Build fails
**Solution:**
```bash
# Test locally first
npm install
node server.js

# If works locally, check:
# - Node version in package.json
# - All dependencies in package.json
```

### Issue: Uploads not persisting
**Expected on free tier!** 
- Ephemeral storage
- Files deleted on restart
- Solution: Add persistent disk (paid plan)

### Issue: App sleeps (free tier)
**Expected behavior:**
- Free tier sleeps after 15 min
- First request takes 30-60 seconds to wake up
- Solution: Upgrade to Starter ($7/mo)

### Issue: "Workspace not found" after upload
**Likely cause:** App restarted, files deleted
**Solution:** 
- Add persistent disk ($1/mo)
- Or implement database storage

---

## 💰 Cost Breakdown

### Free Tier:
- **Cost:** $0/month
- **Limitations:**
  - Sleeps after 15 min inactivity
  - 750 hours/month free
  - Ephemeral storage (files deleted)
  - Slower performance

### Starter Plan:
- **Cost:** $7/month
- **Benefits:**
  - Always on (no sleeping)
  - Better performance
  - Can add persistent disk
  - 512 MB RAM, 0.5 CPU

### With Persistent Storage:
- **Cost:** $7/mo + $1/GB/mo = ~$8/month
- **Benefits:**
  - Files persist across restarts
  - Uploaded workspaces saved
  - Production-ready storage

---

## 📋 Post-Deployment Checklist

After successful deployment:

- [ ] App is accessible at Render URL
- [ ] Upload a test document works
- [ ] Sections are detected correctly
- [ ] Edit and save functionality works
- [ ] Privacy warning is visible
- [ ] Consider adding persistent disk if using regularly
- [ ] Set up custom domain (optional)
- [ ] Share URL with stakeholders
- [ ] Monitor logs for any errors

---

## 🔒 Security Reminder

Your app is now **PUBLIC on the internet**:

- ⚠️ Anyone can access your URL
- ⚠️ Anyone can upload documents
- ⚠️ No authentication or access control
- ⚠️ Not secure for sensitive data

**For production use:**
1. Add authentication system
2. Add access control
3. Use database instead of files
4. Add rate limiting
5. Implement monitoring
6. Add backup system

See `DEPLOYMENT_GUIDE.md` for security enhancements.

---

## 📞 Support

**Render Documentation:**
- https://render.com/docs
- https://render.com/docs/deploy-node-express-app

**Common Issues:**
- https://render.com/docs/troubleshooting

**Community:**
- https://community.render.com

**Support:**
- Email: support@render.com
- Dashboard: Help button

---

## ✅ Quick Reference

```bash
# Update and redeploy:
git add .
git commit -m "Update message"
git push origin main

# View logs:
# Go to: https://dashboard.render.com
# Select your service → Logs tab

# Restart service:
# Dashboard → Manual Deploy → Deploy latest commit
```

---

## 🎉 You're Live!

Your EQUIS SAR MVP is now deployed on Render!

**Your URL:** Check your Render dashboard for the full URL
**Format:** `https://equis-sar-mvp-xxxx.onrender.com`

Share this URL to let others test your application.

**Remember:** Free tier sleeps after 15 min and has ephemeral storage. For production use, upgrade to Starter + Persistent Disk.

---

Need help? Check the logs in your Render dashboard or refer to this guide.
