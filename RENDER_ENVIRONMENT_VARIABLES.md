# Render Environment Variables Configuration

## 🔧 Environment Variables for EQUIS SAR MVP

Based on [Render's Environment Variables documentation](https://render.com/docs/configure-environment-variables), here's what you need to set:

---

## ✅ Required Environment Variables

### Automatic (Render sets these):

| Variable | Value | Description |
|----------|-------|-------------|
| `PORT` | Auto-set by Render | Server port (usually 10000) |
| `NODE_ENV` | Can override | Set to "production" |

**Note:** Render automatically sets `PORT`, so our `server.js` already handles this with:
```javascript
const PORT = process.env.PORT || 3000;
```

---

## 📝 Recommended Environment Variables to Add

### When Creating Your Web Service:

During the "Create Web Service" step on Render, scroll down to **"Environment Variables"** section and add these:

### 1. NODE_ENV (Optional but recommended)
```
Key:   NODE_ENV
Value: production
```
**Purpose:** Tells the app it's running in production mode

### 2. MAX_FILE_SIZE (Optional)
```
Key:   MAX_FILE_SIZE
Value: 10485760
```
**Purpose:** Maximum upload size in bytes (10MB = 10485760 bytes)

---

## 🎯 Step-by-Step: How to Add Environment Variables on Render

### Option A: During Initial Deployment

1. When creating your web service, scroll to **"Environment Variables"**
2. Click **"Add Environment Variable"**
3. Enter:
   - **Key:** `NODE_ENV`
   - **Value:** `production`
4. Click **"Add Environment Variable"** again for more
5. Enter:
   - **Key:** `MAX_FILE_SIZE`
   - **Value:** `10485760`
6. Continue with deployment

### Option B: After Deployment

1. Go to your Render dashboard: https://dashboard.render.com
2. Click on your `equis-sar-mvp` service
3. Click **"Environment"** in the left sidebar
4. Click **"Add Environment Variable"**
5. Add each variable:
   - Key and Value
   - Click "Save Changes"
6. Your service will automatically redeploy

---

## 📊 Complete Environment Variables List

Here's what you should configure:

```bash
# Production mode
NODE_ENV=production

# Maximum file upload size (10MB)
MAX_FILE_SIZE=10485760

# Note: PORT is automatically set by Render, don't add it manually
```

---

## 🔒 Environment Variable Best Practices

### ✅ DO:
- Set `NODE_ENV=production` for production deployments
- Use environment variables for configuration
- Keep sensitive values in environment variables (not in code)
- Document what each variable does

### ❌ DON'T:
- Don't hardcode configuration in code
- Don't commit `.env` files with secrets to git
- Don't manually set `PORT` on Render (it's automatic)
- Don't store API keys in code (though this MVP doesn't use any)

---

## 🎨 Visual Guide: Adding Environment Variables

```
Render Dashboard → Your Service → Environment Tab
┌─────────────────────────────────────────────────────────┐
│  Environment Variables                                  │
│                                                         │
│  ┌──────────────────────────────────────────────────┐  │
│  │  Key                    Value                     │  │
│  ├──────────────────────────────────────────────────┤  │
│  │  NODE_ENV               production               │  │
│  ├──────────────────────────────────────────────────┤  │
│  │  MAX_FILE_SIZE          10485760                 │  │
│  └──────────────────────────────────────────────────┘  │
│                                                         │
│  [+ Add Environment Variable]                          │
│                                                         │
│  [ Save Changes ]                                      │
└─────────────────────────────────────────────────────────┘
```

---

## 🔄 What Happens After Adding Variables

1. Click **"Save Changes"**
2. Render automatically triggers a new deployment
3. Your app restarts with new environment variables
4. Check logs to verify:
   ```
   EQUIS SAR MVP server running on http://localhost:10000
   ```

---

## 🧪 Testing Environment Variables

After deployment, you can verify environment variables are working:

### Check in Render Logs:
Look for messages that use environment variables. If you add logging to `server.js`:

```javascript
console.log('Environment:', process.env.NODE_ENV);
console.log('Port:', process.env.PORT);
console.log('Max file size:', process.env.MAX_FILE_SIZE);
```

---

## 📝 Optional: Create .env.example for Documentation

Create a file to document environment variables (for developers):

```bash
# .env.example
NODE_ENV=production
MAX_FILE_SIZE=10485760
# PORT is set automatically by Render
```

**Important:** Never commit actual `.env` file with real secrets!

---

## ⚡ Quick Reference

### Minimal Setup (Recommended):
Just add one variable during deployment:
```
NODE_ENV=production
```

### Complete Setup:
Add both variables:
```
NODE_ENV=production
MAX_FILE_SIZE=10485760
```

### Nothing Required:
Actually, the app works fine WITHOUT any custom environment variables because:
- Render sets `PORT` automatically ✅
- Our code has sensible defaults ✅

---

## 🎯 My Recommendation

**For your EQUIS SAR MVP, you can deploy with NO custom environment variables!**

The app will work perfectly because:
1. ✅ Render automatically sets `PORT`
2. ✅ Our code defaults to port 3000 locally
3. ✅ File size limits are handled by multer

**However, if you want to be explicit, add:**
```
NODE_ENV=production
```

That's it! One variable is plenty for this MVP.

---

## 🆘 Troubleshooting

### "Application failed to respond"
- ✅ Make sure you're NOT manually setting `PORT`
- ✅ Let Render set `PORT` automatically
- ✅ Code should use: `process.env.PORT || 3000`

### Variables not working?
- Check spelling (case-sensitive!)
- Click "Save Changes" after adding
- Wait for automatic redeployment
- Check logs for the new values

### Need to change a variable?
1. Dashboard → Service → Environment
2. Click the variable to edit
3. Update value
4. Click "Save Changes"
5. App redeploys automatically

---

## ✅ Summary

**What to do:**

1. **During deployment:** 
   - You can leave environment variables **empty** (totally fine!)
   - Or add just one: `NODE_ENV=production`

2. **After deployment (optional):**
   - Go to Environment tab
   - Add `NODE_ENV=production` if you want
   - Click Save Changes

3. **Result:**
   - Your app works either way! ✅

**Bottom line:** Environment variables are optional for this MVP. The app is already configured to work on Render out of the box!

---

## 📚 Additional Resources

- **Render Docs:** https://render.com/docs/configure-environment-variables
- **Environment Groups:** https://render.com/docs/environment-groups
- **Secrets:** https://render.com/docs/using-secrets

---

*The app will work fine without custom environment variables. Add them if you want more explicit configuration.*
