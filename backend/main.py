"""
EQUIS SAR Generation Tool - Main FastAPI Application
Single-user web application for generating formatted EQUIS SAR drafts
"""

from fastapi import FastAPI, UploadFile, File, HTTPException, Form
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse, JSONResponse
from typing import List, Optional
import os
import uuid
import shutil
from pathlib import Path
import json

from services.session_manager import SessionManager
from services.sar_parser import SARParser
from services.equis_parser import EQUISParser
from services.evidence_parser import EvidenceParser
from services.semantic_mapper import SemanticMapper
from services.draft_generator import DraftGenerator
from services.docx_exporter import DOCXExporter
from models.schemas import (
    SessionResponse, 
    ParseResponse, 
    MappingResponse, 
    DraftResponse,
    CoverageDashboard,
    SectionUpdate
)

app = FastAPI(title="EQUIS SAR Generator", version="1.0.0")

# CORS middleware for frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize services
session_manager = SessionManager()
sar_parser = SARParser()
equis_parser = EQUISParser()
evidence_parser = EvidenceParser()
semantic_mapper = SemanticMapper()
draft_generator = DraftGenerator()
docx_exporter = DOCXExporter()

# Store EQUIS standards index globally (loaded once)
EQUIS_STANDARDS_INDEX = None


@app.on_event("startup")
async def startup_event():
    """Initialize the application and load EQUIS standards"""
    global EQUIS_STANDARDS_INDEX
    
    # Check if EQUIS Standards PDF exists
    equis_pdf_path = Path("data/EQUIS_Standards_and_Criteria.pdf")
    if equis_pdf_path.exists():
        print("Loading EQUIS Standards & Criteria...")
        EQUIS_STANDARDS_INDEX = equis_parser.parse_standards_pdf(str(equis_pdf_path))
        print(f"Loaded {len(EQUIS_STANDARDS_INDEX.get('standards', []))} standards")
    else:
        print("WARNING: EQUIS Standards PDF not found. Place at data/EQUIS_Standards_and_Criteria.pdf")
        EQUIS_STANDARDS_INDEX = {"standards": [], "clauses": {}}


@app.get("/")
async def root():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "app": "EQUIS SAR Generator",
        "version": "1.0.0",
        "equis_standards_loaded": EQUIS_STANDARDS_INDEX is not None and len(EQUIS_STANDARDS_INDEX.get("standards", [])) > 0
    }


@app.post("/api/session/create", response_model=SessionResponse)
async def create_session():
    """Create a new SAR generation session"""
    session_id = session_manager.create_session()
    return SessionResponse(
        session_id=session_id,
        status="created",
        message="Session created successfully. Ready to upload files."
    )


@app.post("/api/session/{session_id}/upload-sar")
async def upload_sar(
    session_id: str,
    file: UploadFile = File(...)
):
    """Upload the previous SAR document"""
    if not session_manager.session_exists(session_id):
        raise HTTPException(status_code=404, detail="Session not found")
    
    # Validate file type
    allowed_extensions = [".docx", ".pdf", ".odt", ".txt"]
    file_ext = Path(file.filename).suffix.lower()
    if file_ext not in allowed_extensions:
        raise HTTPException(
            status_code=400, 
            detail=f"Invalid file type. Allowed: {', '.join(allowed_extensions)}"
        )
    
    # Save file
    session_dir = session_manager.get_session_dir(session_id)
    sar_path = session_dir / f"previous_sar{file_ext}"
    
    with open(sar_path, "wb") as f:
        content = await file.read()
        f.write(content)
    
    # Parse SAR
    try:
        parsed_sar = sar_parser.parse_sar(str(sar_path))
        
        # Save parsed structure
        session_manager.save_session_data(session_id, "parsed_sar", parsed_sar)
        
        return JSONResponse({
            "status": "success",
            "message": f"SAR uploaded and parsed successfully",
            "sections_count": len(parsed_sar.get("sections", [])),
            "file_type": file_ext,
            "parsed_structure": parsed_sar
        })
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error parsing SAR: {str(e)}")


@app.post("/api/session/{session_id}/upload-evidence")
async def upload_evidence(
    session_id: str,
    files: List[UploadFile] = File(...)
):
    """Upload supporting evidence files"""
    if not session_manager.session_exists(session_id):
        raise HTTPException(status_code=404, detail="Session not found")
    
    # Validate file types
    allowed_extensions = [".pdf", ".docx", ".xlsx", ".csv", ".pptx", ".png", ".jpg", ".jpeg"]
    
    uploaded_files = []
    session_dir = session_manager.get_session_dir(session_id)
    evidence_dir = session_dir / "evidence"
    evidence_dir.mkdir(exist_ok=True)
    
    for file in files:
        file_ext = Path(file.filename).suffix.lower()
        if file_ext not in allowed_extensions:
            continue
        
        # Save file with unique name
        file_id = str(uuid.uuid4())
        safe_filename = f"{file_id}_{file.filename}"
        file_path = evidence_dir / safe_filename
        
        with open(file_path, "wb") as f:
            content = await file.read()
            f.write(content)
        
        # Parse evidence file
        try:
            parsed_evidence = evidence_parser.parse_file(str(file_path))
            uploaded_files.append({
                "file_id": file_id,
                "filename": file.filename,
                "path": str(file_path),
                "type": file_ext,
                "parsed": parsed_evidence
            })
        except Exception as e:
            print(f"Error parsing {file.filename}: {e}")
            uploaded_files.append({
                "file_id": file_id,
                "filename": file.filename,
                "path": str(file_path),
                "type": file_ext,
                "error": str(e)
            })
    
    # Save evidence index
    session_manager.save_session_data(session_id, "evidence_files", uploaded_files)
    
    return JSONResponse({
        "status": "success",
        "message": f"Uploaded {len(uploaded_files)} evidence files",
        "files": uploaded_files
    })


@app.post("/api/session/{session_id}/generate-draft")
async def generate_draft(session_id: str):
    """Generate the 2026 SAR draft with mapping and suggestions"""
    if not session_manager.session_exists(session_id):
        raise HTTPException(status_code=404, detail="Session not found")
    
    # Load parsed SAR and evidence
    parsed_sar = session_manager.load_session_data(session_id, "parsed_sar")
    evidence_files = session_manager.load_session_data(session_id, "evidence_files")
    
    if not parsed_sar:
        raise HTTPException(status_code=400, detail="No SAR uploaded. Please upload a SAR first.")
    
    if not EQUIS_STANDARDS_INDEX or len(EQUIS_STANDARDS_INDEX.get("standards", [])) == 0:
        raise HTTPException(status_code=500, detail="EQUIS Standards not loaded")
    
    try:
        # Step 1: Map SAR sections to EQUIS criteria
        mapping_results = semantic_mapper.map_sections_to_criteria(
            parsed_sar["sections"],
            EQUIS_STANDARDS_INDEX,
            evidence_files or []
        )
        
        # Step 2: Generate draft with suggestions
        draft = draft_generator.generate_draft(
            parsed_sar,
            mapping_results,
            EQUIS_STANDARDS_INDEX,
            evidence_files or []
        )
        
        # Step 3: Calculate coverage
        coverage = draft_generator.calculate_coverage(
            mapping_results,
            EQUIS_STANDARDS_INDEX
        )
        
        # Save results
        session_manager.save_session_data(session_id, "mapping_results", mapping_results)
        session_manager.save_session_data(session_id, "draft", draft)
        session_manager.save_session_data(session_id, "coverage", coverage)
        
        return JSONResponse({
            "status": "success",
            "message": "Draft generated successfully",
            "draft": draft,
            "coverage": coverage,
            "sections_count": len(draft.get("sections", []))
        })
        
    except Exception as e:
        import traceback
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=f"Error generating draft: {str(e)}")


@app.get("/api/session/{session_id}/draft")
async def get_draft(session_id: str):
    """Get the current draft"""
    if not session_manager.session_exists(session_id):
        raise HTTPException(status_code=404, detail="Session not found")
    
    draft = session_manager.load_session_data(session_id, "draft")
    if not draft:
        raise HTTPException(status_code=404, detail="No draft found. Generate a draft first.")
    
    return JSONResponse(draft)


@app.get("/api/session/{session_id}/coverage")
async def get_coverage(session_id: str):
    """Get coverage dashboard data"""
    if not session_manager.session_exists(session_id):
        raise HTTPException(status_code=404, detail="Session not found")
    
    coverage = session_manager.load_session_data(session_id, "coverage")
    if not coverage:
        raise HTTPException(status_code=404, detail="No coverage data. Generate a draft first.")
    
    return JSONResponse(coverage)


@app.put("/api/session/{session_id}/section/{section_id}")
async def update_section(
    session_id: str,
    section_id: str,
    update: SectionUpdate
):
    """Update a section's content (accept/reject suggestions)"""
    if not session_manager.session_exists(session_id):
        raise HTTPException(status_code=404, detail="Session not found")
    
    draft = session_manager.load_session_data(session_id, "draft")
    if not draft:
        raise HTTPException(status_code=404, detail="No draft found")
    
    # Find and update section
    for section in draft.get("sections", []):
        if section.get("id") == section_id:
            section["content"] = update.content
            if update.accepted_suggestions:
                section["accepted_suggestions"] = update.accepted_suggestions
            if update.rejected_suggestions:
                section["rejected_suggestions"] = update.rejected_suggestions
            break
    
    # Save updated draft
    session_manager.save_session_data(session_id, "draft", draft)
    
    return JSONResponse({"status": "success", "message": "Section updated"})


@app.post("/api/session/{session_id}/export")
async def export_docx(
    session_id: str,
    include_suggestions: bool = Form(False),
    include_footnotes: bool = Form(True),
    include_annex: bool = Form(False)
):
    """Export the draft as a DOCX file"""
    if not session_manager.session_exists(session_id):
        raise HTTPException(status_code=404, detail="Session not found")
    
    draft = session_manager.load_session_data(session_id, "draft")
    if not draft:
        raise HTTPException(status_code=404, detail="No draft found")
    
    try:
        # Generate DOCX
        output_path = session_manager.get_session_dir(session_id) / "EQUIS_SAR_2026_Draft.docx"
        
        docx_exporter.export_to_docx(
            draft=draft,
            output_path=str(output_path),
            include_suggestions=include_suggestions,
            include_footnotes=include_footnotes,
            include_annex=include_annex
        )
        
        return FileResponse(
            path=str(output_path),
            filename="EQUIS_SAR_2026_Draft.docx",
            media_type="application/vnd.openxmlformats-officedocument.wordprocessingml.document"
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error exporting DOCX: {str(e)}")


@app.delete("/api/session/{session_id}")
async def delete_session(session_id: str):
    """Delete a session and all its files"""
    if not session_manager.session_exists(session_id):
        raise HTTPException(status_code=404, detail="Session not found")
    
    session_manager.delete_session(session_id)
    
    return JSONResponse({
        "status": "success",
        "message": "Session deleted successfully. All files removed."
    })


@app.get("/api/equis-standards")
async def get_equis_standards():
    """Get the loaded EQUIS standards structure"""
    if not EQUIS_STANDARDS_INDEX:
        raise HTTPException(status_code=404, detail="EQUIS Standards not loaded")
    
    return JSONResponse(EQUIS_STANDARDS_INDEX)


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
