# EQUIS SAR MVP

A development MVP application for uploading, analyzing, and editing SAR (Suspicious Activity Report) documents.

## Overview

EQUIS SAR MVP allows users to:
- Upload `.docx` or `.doc` SAR documents
- Automatically detect document sections using heuristic analysis
- Create unique workspaces for each document
- Edit section titles and content
- Save changes persistently to local storage

## ⚠️ IMPORTANT PRIVACY & SECURITY NOTICE

**THIS IS A DEVELOPMENT BUILD - NOT FOR PRODUCTION USE**

### Critical Limitations:
- **NO AUTHENTICATION**: Workspaces are public and accessible to anyone with the workspace ID
- **NO ENCRYPTION**: All data is stored in plain text on the local filesystem
- **PUBLIC BY LINK**: Workspace IDs are UUIDs, but anyone who obtains the ID can access the workspace
- **LOCAL STORAGE ONLY**: All files are stored in the `uploads/` directory without backup or redundancy
- **NO PII PROTECTION**: Do NOT upload documents containing sensitive personally identifiable information (PII)

**Use this application only for testing and development purposes with non-sensitive data.**

## Requirements

- Node.js (v14 or higher)
- npm (comes with Node.js)

## Installation

1. Install dependencies:
```bash
npm install
```

2. The `uploads/` directory will be created automatically when you upload your first document.

## Running the Application

Start the server:
```bash
npm start
```

The application will be available at:
```
http://localhost:3000
```

## Usage

### Uploading a Document

1. Navigate to `http://localhost:3000`
2. Read the privacy warning carefully
3. Click "Choose File" and select a `.docx` or `.doc` file
4. Click "Upload Document"
5. You'll be redirected to your unique workspace

### Working with Workspaces

Once in a workspace, you can:
- **View Sections**: See all detected sections in the left sidebar
- **Edit Content**: Click a section to load it in the editor
- **Edit Title**: Modify the section title in the text input
- **Edit Content**: Modify the section content in the textarea
- **Save Changes**: Click "Save Changes" to persist your edits
- **Copy Workspace ID**: Click the 📋 button to copy the workspace ID
- **Upload Another**: Click "Upload Another" to return to the homepage

### Sharing Workspaces

To share a workspace:
1. Copy the workspace ID or the full URL (e.g., `http://localhost:3000/workspace/abc-123-def`)
2. Share the link with others
3. ⚠️ Remember: Anyone with this link can access and edit the workspace

## File Structure

```
/workspace
├── server.js              # Express server with API endpoints
├── package.json           # Node.js dependencies
├── uploads/               # Workspace JSON files (created automatically)
│   └── <workspaceId>.json
├── public/
│   ├── index.html         # Homepage with upload form
│   ├── workspace.html     # Workspace editor page
│   └── styles.css         # Application styles
└── README.md             # This file
```

## API Endpoints

### `POST /api/upload`
Upload a `.docx` or `.doc` file and create a workspace.

**Request**: Multipart form data with `document` field
**Response**: `{ success: true, workspaceId: "uuid" }`

### `GET /api/workspace/:workspaceId`
Retrieve workspace data.

**Response**: Workspace object with sections

### `POST /api/save-section`
Save edited section content.

**Request Body**:
```json
{
  "workspaceId": "uuid",
  "sectionId": 1,
  "title": "Section Title",
  "content": "Section content..."
}
```

**Response**: `{ success: true, section: {...} }`

## Section Detection Heuristics

The application automatically detects document sections using the following heuristics:
- **Numbered headings**: Lines starting with numbers (e.g., "1.", "1.1", "[1]")
- **Short lines**: Lines under 100 characters
- **All caps**: Lines in all uppercase letters
- **Title case**: Lines with title case formatting and special punctuation (colons, em-dashes)
- **Structural elements**: Heading tags from the original document

## File Validation

Both client-side and server-side validation ensures only `.docx` and `.doc` files are accepted:
- **Client-side**: HTML5 `accept` attribute and JavaScript validation
- **Server-side**: Multer file filter checking file extensions

## Data Storage

All workspace data is stored in JSON files under the `uploads/` directory:

```json
{
  "id": "workspace-uuid",
  "filename": "document.docx",
  "createdAt": "2025-12-08T...",
  "contentHtml": "<p>Full HTML content...</p>",
  "sections": [
    {
      "id": 1,
      "title": "Section Title",
      "content": "Section content..."
    }
  ],
  "gapList": []
}
```

## Future Integration Placeholders

This MVP does not include any LLM (Large Language Model) integration. Future versions may include:
- Gap analysis using AI
- Automated section detection improvements
- Content summarization
- Compliance checking

**Note**: No provider-specific code (OpenAI, Anthropic, etc.) or API keys are included in this codebase. Integration points would need to be added separately.

## Troubleshooting

### Port already in use
If port 3000 is already in use, you can change it by setting the PORT environment variable:
```bash
PORT=3001 npm start
```

### Upload fails
- Ensure the file is a valid `.docx` or `.doc` file
- Check that the `uploads/` directory exists and is writable
- Check server logs for detailed error messages

### Workspace not found
- Verify the workspace ID is correct
- Check that the workspace JSON file exists in `uploads/`
- The file should be named `<workspaceId>.json`

## Development Notes

### Technology Stack
- **Backend**: Node.js + Express
- **Document Processing**: mammoth (for .docx to HTML conversion)
- **File Upload**: multer
- **Frontend**: Vanilla HTML/CSS/JavaScript (no framework)
- **Storage**: Local filesystem (JSON files)

### Testing Checklist
- [ ] Upload a `.docx` file successfully
- [ ] Verify sections appear in sidebar
- [ ] Click a section and verify it loads in the editor
- [ ] Edit section title and content
- [ ] Click "Save Changes" and verify success message
- [ ] Verify `uploads/<workspaceId>.json` contains updated content
- [ ] Try uploading a non-.docx file and verify rejection
- [ ] Copy workspace ID and open in new browser tab
- [ ] Verify privacy warnings are displayed prominently

## License

See LICENSE file for details.

## Support

This is a development MVP. For issues or questions, refer to the project documentation or contact the development team.
