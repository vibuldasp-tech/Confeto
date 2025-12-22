# EQUIS SAR Generator - Backend

Python FastAPI backend for the EQUIS SAR Generation Tool.

## Setup

1. Create virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Place EQUIS Standards PDF:
- Create a `data/` directory
- Place the EQUIS Standards & Criteria PDF as `data/EQUIS_Standards_and_Criteria.pdf`

## Run

```bash
python main.py
```

Or with uvicorn:
```bash
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

## API Endpoints

- `POST /api/session/create` - Create new session
- `POST /api/session/{id}/upload-sar` - Upload SAR document
- `POST /api/session/{id}/upload-evidence` - Upload evidence files
- `POST /api/session/{id}/generate-draft` - Generate draft
- `GET /api/session/{id}/draft` - Get draft
- `GET /api/session/{id}/coverage` - Get coverage dashboard
- `PUT /api/session/{id}/section/{section_id}` - Update section
- `POST /api/session/{id}/export` - Export to DOCX
- `DELETE /api/session/{id}` - Delete session

## Structure

- `main.py` - FastAPI application
- `models/` - Pydantic schemas
- `services/` - Business logic
  - `session_manager.py` - Session handling
  - `sar_parser.py` - Parse uploaded SAR
  - `equis_parser.py` - Parse EQUIS standards
  - `evidence_parser.py` - Parse evidence files
  - `semantic_mapper.py` - Map sections to criteria
  - `draft_generator.py` - Generate draft with suggestions
  - `docx_exporter.py` - Export to Word
