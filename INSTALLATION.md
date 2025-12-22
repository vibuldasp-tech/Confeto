# EQUIS SAR Generator - Installation Guide

This guide will walk you through setting up the EQUIS SAR Generation Tool on your local machine.

## Prerequisites

Before you begin, ensure you have the following installed:

1. **Python 3.8 or higher**
   - Download from: https://www.python.org/downloads/
   - Verify: `python --version` or `python3 --version`

2. **Node.js 16 or higher**
   - Download from: https://nodejs.org/
   - Verify: `node --version`

3. **npm (comes with Node.js)**
   - Verify: `npm --version`

4. **(Optional) Tesseract OCR** - Only needed for scanned PDF support
   - macOS: `brew install tesseract`
   - Ubuntu: `sudo apt-get install tesseract-ocr`
   - Windows: Download from https://github.com/UB-Mannheim/tesseract/wiki

## Step 1: Clone or Download the Project

```bash
# If you have the project as a zip, extract it
# Then navigate to the project directory
cd equis-sar-generator
```

## Step 2: Backend Setup

### 2.1 Navigate to Backend Directory

```bash
cd backend
```

### 2.2 Create Python Virtual Environment

**On macOS/Linux:**
```bash
python3 -m venv venv
source venv/bin/activate
```

**On Windows:**
```bash
python -m venv venv
venv\Scripts\activate
```

You should see `(venv)` in your terminal prompt.

### 2.3 Install Python Dependencies

```bash
pip install -r requirements.txt
```

This may take a few minutes as it downloads all required packages.

### 2.4 Place EQUIS Standards PDF

1. Create a `data` directory if it doesn't exist:
```bash
mkdir data
```

2. Place your EQUIS Standards & Criteria PDF in the data directory:
```bash
# Copy your PDF to:
# backend/data/EQUIS_Standards_and_Criteria.pdf
```

**Note:** If you don't have the EQUIS PDF, the system will work with mock standards for testing purposes.

### 2.5 Test Backend

```bash
python main.py
```

You should see:
```
INFO:     Started server process
INFO:     Uvicorn running on http://0.0.0.0:8000
```

Open http://localhost:8000 in your browser. You should see:
```json
{
  "status": "healthy",
  "app": "EQUIS SAR Generator",
  "version": "1.0.0"
}
```

**Keep this terminal window open** (backend must run continuously).

## Step 3: Frontend Setup

Open a **NEW terminal window** (keep backend running in the first one).

### 3.1 Navigate to Frontend Directory

```bash
cd frontend  # If you're in the root directory
# OR
cd ../frontend  # If you're in the backend directory
```

### 3.2 Install Node Dependencies

```bash
npm install
```

This will take a few minutes.

### 3.3 Start Development Server

```bash
npm run dev
```

You should see:
```
  VITE v5.x.x  ready in xxx ms

  ➜  Local:   http://localhost:5173/
  ➜  Network: use --host to expose
```

### 3.4 Open the Application

Open http://localhost:5173 in your web browser.

You should see the EQUIS SAR Generator onboarding screen with a purple gradient background.

## Step 4: Verify Installation

1. **Check Backend Health**
   - Visit: http://localhost:8000
   - Should show JSON with "status": "healthy"

2. **Check Frontend**
   - Visit: http://localhost:5173
   - Should show the onboarding screen with "EQUIS SAR Generator" title

3. **Test File Upload**
   - Try uploading a test document (any .txt file works for testing)
   - Should show upload progress

## Troubleshooting

### Backend Issues

**Problem: Port 8000 already in use**
```bash
# Find and kill the process using port 8000
# On macOS/Linux:
lsof -ti:8000 | xargs kill -9

# On Windows:
netstat -ano | findstr :8000
taskkill /PID <PID> /F
```

**Problem: Missing Python packages**
```bash
# Ensure virtual environment is activated
source venv/bin/activate  # macOS/Linux
venv\Scripts\activate      # Windows

# Reinstall dependencies
pip install -r requirements.txt
```

**Problem: ImportError for sentence-transformers**
```bash
# This is a large package, may take time to download
pip install --upgrade sentence-transformers
```

### Frontend Issues

**Problem: Port 5173 already in use**
```bash
# Edit vite.config.js and change the port
# OR kill the process using port 5173
```

**Problem: Cannot connect to backend**
- Ensure backend is running on port 8000
- Check `vite.config.js` proxy settings
- Check browser console for CORS errors

**Problem: npm install fails**
```bash
# Clear npm cache and try again
npm cache clean --force
npm install
```

### General Issues

**Problem: Python version too old**
```bash
# Check version
python --version

# If < 3.8, download latest from python.org
```

**Problem: Node version too old**
```bash
# Check version
node --version

# If < 16, download latest from nodejs.org
```

## Running the Application

Once installed, you'll need **two terminal windows** every time you use the app:

**Terminal 1 - Backend:**
```bash
cd backend
source venv/bin/activate  # or venv\Scripts\activate on Windows
python main.py
```

**Terminal 2 - Frontend:**
```bash
cd frontend
npm run dev
```

Then open http://localhost:5173 in your browser.

## Stopping the Application

1. In each terminal window, press `Ctrl+C`
2. Deactivate Python virtual environment: `deactivate`

## Next Steps

- Read the main README.md for usage instructions
- Place your EQUIS Standards PDF in backend/data/
- Prepare your 2022 SAR and evidence files for upload
- Try the onboarding flow

## Getting Help

If you encounter issues:
1. Check the error messages in both terminal windows
2. Review the troubleshooting section above
3. Check that all prerequisites are correctly installed
4. Ensure ports 8000 and 5173 are available

## System Requirements

**Minimum:**
- 4GB RAM
- 2GB free disk space
- Modern web browser (Chrome, Firefox, Safari, Edge)

**Recommended:**
- 8GB+ RAM (for large documents and semantic processing)
- SSD storage
- Stable internet connection (for initial model download)
