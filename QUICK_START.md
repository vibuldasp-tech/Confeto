# EQUIS SAR Generator - Quick Start

Get up and running in 5 minutes!

## Prerequisites

- Python 3.8+
- Node.js 16+
- Your 2022 SAR and evidence files ready

## Installation

### Option 1: Use the Startup Script (Recommended)

**On macOS/Linux:**
```bash
./start.sh
```

**On Windows:**
```
start.bat
```

The script will:
- Check prerequisites
- Create virtual environments
- Install dependencies
- Start both servers
- Open the app in your browser

### Option 2: Manual Setup

**Terminal 1 - Backend:**
```bash
cd backend
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
python main.py
```

**Terminal 2 - Frontend:**
```bash
cd frontend
npm install
npm run dev
```

## First Time Setup

1. **Place EQUIS PDF** (optional but recommended):
   - Put your EQUIS Standards & Criteria PDF in `backend/data/`
   - Name it: `EQUIS_Standards_and_Criteria.pdf`

2. **Open the app**:
   - Go to http://localhost:5173
   - You should see the purple onboarding screen

## Basic Usage

1. **Upload your 2022 SAR** (.docx, .pdf, or .txt)
2. **Upload evidence files** (PDFs, Word, Excel, PowerPoint, images)
3. **Click "Generate Draft"** (takes 1-2 minutes)
4. **Edit sections** and **accept/reject suggestions**
5. **Check coverage** in the dashboard
6. **Export to Word** when finished

## First Time Tips

- Upload complete SAR, not individual sections
- Upload all evidence at once in step 2
- Use text-based PDFs (not scanned images)
- Give descriptive names to evidence files
- Accept high-confidence suggestions first
- Save changes frequently
- Export before deleting session

## Troubleshooting

**Backend won't start:**
```bash
# Check if port 8000 is free
lsof -ti:8000 | xargs kill -9  # macOS/Linux
netstat -ano | findstr :8000   # Windows
```

**Frontend won't start:**
```bash
# Clear npm cache
npm cache clean --force
npm install
```

**Can't connect:**
- Ensure both servers are running
- Check http://localhost:8000 (backend health check)
- Check http://localhost:5173 (frontend)

## Next Steps

- Read USAGE_GUIDE.md for detailed instructions
- Read INSTALLATION.md for full setup guide
- Read README.md for technical details

## Support

- Check inline help tooltips in the app
- Review the yellow banner messages
- Refer to the coverage dashboard for guidance

---

**Ready to go?** Run the startup script and open http://localhost:5173!
