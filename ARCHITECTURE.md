# EQUIS SAR Generator - Architecture Overview

## System Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                         User Browser                        │
│                     (React Frontend)                        │
│                  http://localhost:5173                      │
└────────────────────────┬────────────────────────────────────┘
                         │ HTTP/REST API
                         ▼
┌─────────────────────────────────────────────────────────────┐
│                    FastAPI Backend                          │
│                  http://localhost:8000                      │
│                                                             │
│  ┌──────────────────────────────────────────────────────┐  │
│  │              API Endpoints                           │  │
│  │  /api/session/create                                 │  │
│  │  /api/session/{id}/upload-sar                        │  │
│  │  /api/session/{id}/upload-evidence                   │  │
│  │  /api/session/{id}/generate-draft                    │  │
│  │  /api/session/{id}/draft                             │  │
│  │  /api/session/{id}/coverage                          │  │
│  │  /api/session/{id}/section/{section_id}             │  │
│  │  /api/session/{id}/export                            │  │
│  │  /api/session/{id}                                   │  │
│  └──────────────────────────────────────────────────────┘  │
│                         │                                   │
│                         ▼                                   │
│  ┌──────────────────────────────────────────────────────┐  │
│  │              Service Layer                           │  │
│  │                                                      │  │
│  │  ┌─────────────────┐  ┌──────────────────┐          │  │
│  │  │ Session Manager │  │  SAR Parser      │          │  │
│  │  └─────────────────┘  └──────────────────┘          │  │
│  │                                                      │  │
│  │  ┌─────────────────┐  ┌──────────────────┐          │  │
│  │  │ EQUIS Parser    │  │ Evidence Parser  │          │  │
│  │  └─────────────────┘  └──────────────────┘          │  │
│  │                                                      │  │
│  │  ┌─────────────────┐  ┌──────────────────┐          │  │
│  │  │ Semantic Mapper │  │ Draft Generator  │          │  │
│  │  └─────────────────┘  └──────────────────┘          │  │
│  │                                                      │  │
│  │  ┌─────────────────┐                                │  │
│  │  │  DOCX Exporter  │                                │  │
│  │  └─────────────────┘                                │  │
│  └──────────────────────────────────────────────────────┘  │
│                         │                                   │
│                         ▼                                   │
│  ┌──────────────────────────────────────────────────────┐  │
│  │              Data Storage                            │  │
│  │                                                      │  │
│  │  sessions/                                           │  │
│  │    └── {session-id}/                                 │  │
│  │        ├── metadata.json                             │  │
│  │        ├── previous_sar.docx                         │  │
│  │        ├── parsed_sar.json                           │  │
│  │        ├── evidence/                                 │  │
│  │        │   ├── file1.pdf                             │  │
│  │        │   └── file2.docx                            │  │
│  │        ├── evidence_files.json                       │  │
│  │        ├── mapping_results.json                      │  │
│  │        ├── draft.json                                │  │
│  │        ├── coverage.json                             │  │
│  │        └── EQUIS_SAR_2026_Draft.docx                 │  │
│  │                                                      │  │
│  │  data/                                               │  │
│  │    └── EQUIS_Standards_and_Criteria.pdf             │  │
│  └──────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────┘
```

## Frontend Architecture

```
src/
├── main.jsx                    # React entry point
├── App.jsx                     # Main app component
│
├── components/
│   ├── Onboarding.jsx         # File upload wizard
│   ├── TopBar.jsx             # Navigation & actions
│   ├── MainEditor.jsx         # 3-pane layout controller
│   ├── SectionNavigator.jsx   # Left sidebar (section tree)
│   ├── RichTextEditor.jsx     # Center panel (editor)
│   ├── EvidencePanel.jsx      # Right sidebar (evidence)
│   └── CoverageDashboard.jsx  # Coverage analytics
│
├── services/
│   └── api.js                 # API client (axios)
│
└── styles/
    ├── global.css             # Global styles & variables
    └── *.css                  # Component-specific styles
```

## Backend Service Flow

### 1. Session Creation
```
User → POST /api/session/create
     → SessionManager.create_session()
     → Returns session_id
```

### 2. File Upload
```
User → POST /api/session/{id}/upload-sar
     → Save file to sessions/{id}/
     → SARParser.parse_sar()
     → Extract sections, headings, content
     → Save parsed_sar.json
     → Return sections count

User → POST /api/session/{id}/upload-evidence
     → Save files to sessions/{id}/evidence/
     → EvidenceParser.parse_file() for each
     → Extract text, build index
     → Save evidence_files.json
     → Return file list
```

### 3. Draft Generation
```
User → POST /api/session/{id}/generate-draft
     → Load parsed_sar.json
     → Load evidence_files.json
     → Load EQUIS standards index
     
     → SemanticMapper.map_sections_to_criteria()
       ├── Encode SAR sections (sentence-transformers)
       ├── Encode EQUIS criteria
       ├── Calculate semantic similarity
       ├── Find evidence matches
       └── Return mapping_results.json
     
     → DraftGenerator.generate_draft()
       ├── Calculate carry-forward scores
       ├── Generate refinement suggestions
       ├── Generate rewrite suggestions
       ├── Create evidence citations
       ├── Apply default improvements
       └── Return draft.json
     
     → DraftGenerator.calculate_coverage()
       ├── Check criteria coverage
       ├── Calculate per-standard scores
       ├── Identify priority tasks
       └── Return coverage.json
     
     → Save all results
     → Return draft + coverage
```

### 4. Section Updates
```
User → PUT /api/session/{id}/section/{section_id}
     → Load draft.json
     → Update section content
     → Update accepted/rejected suggestions
     → Save draft.json
     → Return success
```

### 5. Export
```
User → POST /api/session/{id}/export
     → Load draft.json
     → DOCXExporter.export_to_docx()
       ├── Create Word document
       ├── Add title & metadata
       ├── Add sections with content
       ├── Add evidence footnotes (optional)
       ├── Add inline suggestions (optional)
       ├── Add suggestions annex (optional)
       └── Save .docx file
     → Return file download
```

### 6. Session Cleanup
```
User → DELETE /api/session/{id}
     → SessionManager.delete_session()
     → Remove entire sessions/{id}/ directory
     → Return success
```

## Data Flow

### Parsing Flow
```
Uploaded SAR
    ↓
SARParser
    ├── DOCX → python-docx → Extract paragraphs, styles, tables
    ├── PDF → PyMuPDF → Extract text, handle OCR if needed
    ├── ODT → Convert to text
    └── TXT → Parse line by line
    ↓
Structured JSON
    {
      sections: [
        { id, number, title, level, content, original_text }
      ],
      tables: [...],
      total_sections: N
    }
```

### Mapping Flow
```
SAR Sections + EQUIS Criteria + Evidence
    ↓
SemanticMapper (sentence-transformers)
    ├── Encode all texts as embeddings
    ├── Calculate cosine similarity
    ├── Threshold-based matching
    └── Keyword fallback
    ↓
Mapping Results
    {
      section_id,
      matched_criteria: [{ criterion, text, similarity }],
      coverage_score: 0-100,
      evidence_matches: [{ file, confidence, excerpts }],
      gaps: [...]
    }
```

### Suggestion Generation Flow
```
Original Content + Mappings + EQUIS Standards
    ↓
DraftGenerator
    ├── Calculate carry-forward score
    │   ├── Check criteria match quality
    │   ├── Detect dated content
    │   └── Check evidence references
    │
    ├── High carry-forward (>0.7)
    │   ├── Date update suggestions
    │   ├── EQUIS reference additions
    │   └── Evidence citation suggestions
    │
    └── Low carry-forward (<0.7)
        ├── Rewrite suggestions
        ├── Content structure recommendations
        └── Evidence gap warnings
    ↓
Suggestions JSON
    {
      id,
      type: "insertion" | "replacement" | "deletion",
      position,
      original_text,
      suggested_text,
      rationale,
      equis_clause,
      equis_clause_number,
      confidence,
      accepted: null | true | false
    }
```

## Key Technologies

### Backend
- **FastAPI**: Modern Python web framework
- **PyMuPDF (fitz)**: PDF parsing
- **python-docx**: Word document reading/writing
- **sentence-transformers**: Semantic similarity (all-MiniLM-L6-v2)
- **pytesseract**: OCR for scanned documents
- **pandas**: Spreadsheet processing
- **python-pptx**: PowerPoint parsing

### Frontend
- **React 18**: UI framework
- **Vite**: Build tool
- **Axios**: HTTP client
- **React Dropzone**: File upload
- **Lucide React**: Icon library

## Security Considerations

### Data Privacy
- Session-based storage only
- No persistent database
- Files deleted on session end
- No external API calls (except model download)

### Input Validation
- File type validation (extension + MIME type)
- File size limits
- Path traversal prevention
- Session ID validation

### CORS
- Configured for localhost development
- Should be restricted in production

## Performance Considerations

### Backend
- Semantic model loaded once on startup
- Lazy evaluation where possible
- Session cleanup cron job recommended
- Large file handling with streaming

### Frontend
- Code splitting by route
- Lazy loading for heavy components
- Debounced save operations
- Pagination for large section lists

## Scalability Notes

### Current Limitations (Single-User)
- In-memory session storage
- No concurrent session handling
- No user authentication
- No database

### To Scale (Future)
- Add PostgreSQL for session storage
- Implement user authentication (OAuth2)
- Add Redis for caching
- Containerize with Docker
- Deploy with load balancer
- Add background job queue (Celery)

## Deployment Architecture

```
┌─────────────────────────────────────────────────────┐
│                   Production Setup                  │
│                                                     │
│  ┌──────────┐         ┌──────────┐                 │
│  │  Nginx   │────────▶│  React   │                 │
│  │  Proxy   │         │  (Static)│                 │
│  └────┬─────┘         └──────────┘                 │
│       │                                             │
│       │ /api/*                                      │
│       ▼                                             │
│  ┌──────────┐                                       │
│  │ Uvicorn  │                                       │
│  │ (FastAPI)│                                       │
│  └────┬─────┘                                       │
│       │                                             │
│       ▼                                             │
│  ┌──────────┐                                       │
│  │ Sessions │                                       │
│  │ (Volume) │                                       │
│  └──────────┘                                       │
└─────────────────────────────────────────────────────┘
```

## Error Handling

### Backend
- Try-catch blocks in all service methods
- HTTP exceptions with descriptive messages
- Logging for debugging
- Graceful degradation (e.g., mock EQUIS if PDF missing)

### Frontend
- Error boundaries for React components
- User-friendly error messages
- Network error handling
- Loading states for async operations

## Testing Strategy

### Backend Testing (Recommended)
- Unit tests for parsers
- Integration tests for API endpoints
- Mock file uploads
- Test with various file formats

### Frontend Testing (Recommended)
- Component tests with React Testing Library
- E2E tests with Playwright/Cypress
- Accessibility testing
- Responsive design testing

## Monitoring & Logging

### Backend
- FastAPI built-in logging
- Session creation/deletion logs
- File upload/parsing logs
- Error logs with stack traces

### Frontend
- Console logging for development
- Error tracking (Sentry recommended for production)
- Performance monitoring (Web Vitals)

---

This architecture supports a single-user, session-based workflow with emphasis on simplicity, privacy, and ease of use for non-technical users.
