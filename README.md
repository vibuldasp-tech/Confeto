# EQUIS SAR Generation Tool

A single-user web application to generate fully formatted draft 2026 EQUIS SAR documents from uploaded previous SARs and supporting evidence files.

## Features

- **Simple Onboarding**: One-step upload process for previous SAR and evidence files
- **Smart Parsing**: Extract structure from DOCX, PDF, ODT, and TXT files
- **Semantic Mapping**: AI-powered mapping of SAR sections to EQUIS standards and criteria
- **Intelligent Suggestions**: Carry-forward text identification and new content recommendations
- **Evidence Linking**: Automatic citation of supporting documents with confidence scores
- **Interactive Editor**: Three-pane layout with section navigator, rich text editor, and evidence panel
- **Toggle Suggestions**: Show/hide AI suggestions with inline accept/reject functionality
- **Coverage Dashboard**: Visual analysis of EQUIS standards coverage
- **DOCX Export**: Export to Word with optional footnotes, suggestions, and annexes
- **Session-Based**: All data is ephemeral and deleted at session end

## Architecture

### Backend (Python FastAPI)
- Document parsing services (SAR, EQUIS Standards, Evidence)
- Semantic mapping using sentence-transformers
- Draft generation with carry-forward detection
- DOCX export functionality
- Session management

### Frontend (React + Vite)
- Modern, intuitive UI with three-pane layout
- Rich text editor with suggestions
- File upload with drag-and-drop
- Real-time coverage dashboard
- Responsive design

## Setup

### Prerequisites
- Python 3.8+
- Node.js 16+
- npm or yarn

### Backend Setup

1. Navigate to backend directory:
```bash
cd backend
```

2. Create virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Place EQUIS Standards PDF:
```bash
mkdir data
# Place EQUIS_Standards_and_Criteria.pdf in data/ directory
```

5. Run the backend:
```bash
python main.py
```

The backend will run on `http://localhost:8000`

### Frontend Setup

1. Navigate to frontend directory:
```bash
cd frontend
```

2. Install dependencies:
```bash
npm install
```

3. Run the development server:
```bash
npm run dev
```

The frontend will run on `http://localhost:5173`

## Usage

1. **Onboarding**
   - Upload your previous SAR (2022 SAR recommended)
   - Upload supporting evidence files (PDFs, DOCX, XLSX, PPTX, images)
   - Click "Generate Draft"

2. **Editor**
   - Browse sections in the left navigator
   - Edit content in the main editor
   - Toggle "Show Suggestions" to view AI recommendations
   - Accept or reject suggestions inline
   - View linked evidence in the right panel

3. **Coverage Dashboard**
   - View overall EQUIS standards coverage
   - See per-standard breakdown
   - Review priority action items

4. **Export**
   - Click the download icon in the top bar
   - Select export options (footnotes, suggestions, annex)
   - Download your DOCX file

5. **End Session**
   - Click the trash icon to delete session
   - All files and generated content will be removed

## Project Structure

```
/
├── backend/
│   ├── main.py                 # FastAPI application
│   ├── requirements.txt        # Python dependencies
│   ├── models/
│   │   └── schemas.py         # Pydantic models
│   ├── services/
│   │   ├── session_manager.py
│   │   ├── sar_parser.py
│   │   ├── equis_parser.py
│   │   ├── evidence_parser.py
│   │   ├── semantic_mapper.py
│   │   ├── draft_generator.py
│   │   └── docx_exporter.py
│   └── data/                  # Place EQUIS PDF here
│
├── frontend/
│   ├── src/
│   │   ├── components/        # React components
│   │   │   ├── Onboarding.jsx
│   │   │   ├── TopBar.jsx
│   │   │   ├── MainEditor.jsx
│   │   │   ├── SectionNavigator.jsx
│   │   │   ├── RichTextEditor.jsx
│   │   │   ├── EvidencePanel.jsx
│   │   │   └── CoverageDashboard.jsx
│   │   ├── services/
│   │   │   └── api.js         # API client
│   │   ├── styles/            # CSS files
│   │   ├── App.jsx
│   │   └── main.jsx
│   ├── package.json
│   └── vite.config.js
│
└── README.md
```

## API Endpoints

- `POST /api/session/create` - Create new session
- `POST /api/session/{id}/upload-sar` - Upload SAR document
- `POST /api/session/{id}/upload-evidence` - Upload evidence files
- `POST /api/session/{id}/generate-draft` - Generate draft with suggestions
- `GET /api/session/{id}/draft` - Get current draft
- `GET /api/session/{id}/coverage` - Get coverage dashboard data
- `PUT /api/session/{id}/section/{section_id}` - Update section content
- `POST /api/session/{id}/export` - Export to DOCX
- `DELETE /api/session/{id}` - Delete session

## Key Features Explained

### Semantic Mapping
The tool uses sentence-transformers to semantically match SAR section content with EQUIS criteria. This provides:
- Coverage scores for each section
- Identification of relevant standards
- Gap analysis

### Carry-Forward Detection
The system analyzes existing content to determine if it can be reused:
- High confidence (>70%): Light edits suggested
- Low confidence (<70%): Major rewrite recommended

### Evidence Linking
Automatically matches evidence files to section content:
- High confidence links (>70%): Auto-cite with footnotes
- Medium confidence (40-70%): Suggest citation
- Low confidence (<40%): Flag as uncertain

### Suggestions System
AI-generated suggestions include:
- Type: insertion, replacement, deletion
- Rationale: Clear explanation
- EQUIS clause: Exact citation from Standards PDF
- Confidence score
- Accept/reject actions

## Notes

- **EQUIS Standards PDF**: Place the official EQUIS Standards & Criteria PDF in `backend/data/` directory. If not provided, the system will use mock standards for development.
- **OCR**: For scanned PDFs, pytesseract with Tesseract OCR must be installed on the system.
- **Session Storage**: All sessions are stored in `backend/sessions/` and should be cleaned up regularly.
- **Non-persistent**: The app does not store institutional data across sessions by design.

## Security & Privacy

- All processing occurs server-side
- No data is sent to external services (except if using OpenAI embeddings)
- Session-based storage only
- Clear session deletion functionality
- All uploaded content treated as confidential

## Development

### Running in Development Mode

Backend:
```bash
cd backend
uvicorn main:app --reload
```

Frontend:
```bash
cd frontend
npm run dev
```

### Building for Production

Frontend:
```bash
cd frontend
npm run build
```

The build output will be in `frontend/dist/`

## Troubleshooting

**Backend won't start:**
- Ensure all Python dependencies are installed
- Check that port 8000 is available
- Verify Python version (3.8+)

**Frontend won't connect to backend:**
- Check that backend is running on port 8000
- Verify CORS settings in backend/main.py
- Check browser console for errors

**PDF parsing fails:**
- Ensure PyMuPDF is properly installed
- For OCR, install Tesseract OCR system package
- Try re-uploading with higher quality PDF

**Semantic mapping not working:**
- First run may be slow as model downloads
- Ensure internet connection for initial model download
- Check sentence-transformers installation

## License

See LICENSE file for details.

## Support

For issues and questions, please refer to the inline help tooltips in the application or review the EQUIS Standards documentation.
