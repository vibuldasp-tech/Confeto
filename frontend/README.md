# EQUIS SAR Generator - Frontend

React + Vite frontend for the EQUIS SAR Generation Tool.

## Features

- Modern, responsive UI
- Three-pane layout (navigator, editor, evidence)
- File upload with drag-and-drop
- Rich text editor with inline suggestions
- Coverage dashboard with visual analytics
- Real-time section editing
- DOCX export with options

## Tech Stack

- React 18
- Vite
- Axios for API calls
- React Dropzone for file uploads
- Lucide React for icons
- Custom CSS (no framework for simplicity)

## Development

```bash
npm install
npm run dev
```

## Build

```bash
npm run build
```

Output will be in `dist/` directory.

## Components

- **Onboarding**: File upload wizard (3 steps)
- **TopBar**: Navigation and actions
- **MainEditor**: Three-pane layout with section editing
- **SectionNavigator**: Left sidebar with section tree
- **RichTextEditor**: Main content editor with suggestions
- **EvidencePanel**: Right sidebar showing linked evidence
- **CoverageDashboard**: Visual analytics of EQUIS coverage

## API Integration

All API calls are in `src/services/api.js`. The frontend communicates with the FastAPI backend on port 8000.

## Styling

CSS files are co-located with components. Global styles are in `src/styles/global.css`.

Color scheme and design tokens are defined as CSS variables in the global stylesheet.
