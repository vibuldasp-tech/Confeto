const express = require('express');
const multer = require('multer');
const mammoth = require('mammoth');
const { v4: uuidv4 } = require('uuid');
const fs = require('fs').promises;
const path = require('path');

const app = express();
const PORT = process.env.PORT || 3000;

// Middleware
app.use(express.json());
app.use(express.urlencoded({ extended: true }));
app.use(express.static('public'));

// Configure multer for file uploads
const storage = multer.diskStorage({
  destination: (req, file, cb) => {
    cb(null, 'uploads/');
  },
  filename: (req, file, cb) => {
    cb(null, `temp-${Date.now()}-${file.originalname}`);
  }
});

const upload = multer({
  storage: storage,
  fileFilter: (req, file, cb) => {
    // Server-side validation: only .docx and .doc files
    const ext = path.extname(file.originalname).toLowerCase();
    if (ext === '.docx' || ext === '.doc') {
      cb(null, true);
    } else {
      cb(new Error('Only .docx and .doc files are allowed'));
    }
  }
});

// Helper function to detect sections from HTML
function detectSections(html) {
  const sections = [];
  
  // More sophisticated approach: parse HTML looking for heading tags
  // Match heading tags (<h1>, <h2>, etc.) and paragraph tags
  const elementRegex = /<(h[1-6]|p)[^>]*>(.*?)<\/\1>/gi;
  const elements = [];
  let match;
  
  while ((match = elementRegex.exec(html)) !== null) {
    const tagName = match[1].toLowerCase();
    const content = match[2].trim();
    elements.push({ tag: tagName, content: content });
  }
  
  let currentSection = null;
  let sectionId = 0;
  
  for (let i = 0; i < elements.length; i++) {
    const element = elements[i];
    const plainText = element.content.replace(/<[^>]*>/g, '').trim();
    
    if (!plainText) continue;
    
    // Check if this is a heading element
    const isHeadingTag = /^h[1-6]$/.test(element.tag);
    
    // Additional heuristics for paragraphs that look like headings
    const isShort = plainText.length < 100;
    const hasNumbering = /^(\d+\.|\d+\.\d+|\[?\d+\]?)/.test(plainText);
    const isAllCaps = plainText === plainText.toUpperCase() && plainText.length > 2 && /[A-Z]/.test(plainText);
    const hasStrongTag = /<strong>/i.test(element.content) || /<b>/i.test(element.content);
    
    // A line is a heading if:
    // 1. It's an actual HTML heading tag (h1-h6)
    // 2. OR it has strong/bold formatting AND (is numbered OR is all caps)
    const isHeading = isHeadingTag || (isShort && hasStrongTag && (hasNumbering || isAllCaps));
    
    if (isHeading) {
      // Start a new section
      if (currentSection) {
        sections.push(currentSection);
      }
      sectionId++;
      currentSection = {
        id: sectionId,
        title: plainText.substring(0, 80), // Limit title length
        content: ''
      };
    } else if (currentSection) {
      // Add content to current section
      currentSection.content += element.content + '\n';
    } else {
      // No section yet, create an initial one with the content
      sectionId++;
      currentSection = {
        id: sectionId,
        title: plainText.substring(0, 80),
        content: ''
      };
    }
  }
  
  // Add the last section
  if (currentSection) {
    sections.push(currentSection);
  }
  
  // If no sections were detected, create one default section
  if (sections.length === 0) {
    sections.push({
      id: 1,
      title: 'Document Content',
      content: html
    });
  }
  
  return sections;
}

// API: Upload .docx file and create workspace
app.post('/api/upload', upload.single('document'), async (req, res) => {
  try {
    if (!req.file) {
      return res.status(400).json({ error: 'No file uploaded' });
    }
    
    const tempFilePath = req.file.path;
    const originalFilename = req.file.originalname;
    
    // Extract .docx to HTML
    const result = await mammoth.convertToHtml({ path: tempFilePath });
    const contentHtml = result.value;
    
    // Detect sections using heuristics
    const sections = detectSections(contentHtml);
    
    // Create workspace with UUID
    const workspaceId = uuidv4();
    const workspace = {
      id: workspaceId,
      filename: originalFilename,
      createdAt: new Date().toISOString(),
      contentHtml: contentHtml,
      sections: sections,
      gapList: [] // Placeholder for future gap analysis
    };
    
    // Save workspace to JSON file
    const workspacePath = path.join('uploads', `${workspaceId}.json`);
    await fs.writeFile(workspacePath, JSON.stringify(workspace, null, 2));
    
    // Delete temporary uploaded file
    await fs.unlink(tempFilePath);
    
    res.json({ 
      success: true, 
      workspaceId: workspaceId,
      message: 'Workspace created successfully'
    });
    
  } catch (error) {
    console.error('Upload error:', error);
    res.status(500).json({ 
      error: 'Failed to process document',
      message: error.message 
    });
  }
});

// API: Get workspace data
app.get('/api/workspace/:workspaceId', async (req, res) => {
  try {
    const { workspaceId } = req.params;
    const workspacePath = path.join('uploads', `${workspaceId}.json`);
    
    const data = await fs.readFile(workspacePath, 'utf-8');
    const workspace = JSON.parse(data);
    
    res.json(workspace);
  } catch (error) {
    if (error.code === 'ENOENT') {
      res.status(404).json({ error: 'Workspace not found' });
    } else {
      res.status(500).json({ error: 'Failed to load workspace' });
    }
  }
});

// API: Save edited section
app.post('/api/save-section', async (req, res) => {
  try {
    const { workspaceId, sectionId, title, content } = req.body;
    
    if (!workspaceId || !sectionId) {
      return res.status(400).json({ error: 'Missing required fields' });
    }
    
    const workspacePath = path.join('uploads', `${workspaceId}.json`);
    
    // Read current workspace
    const data = await fs.readFile(workspacePath, 'utf-8');
    const workspace = JSON.parse(data);
    
    // Find and update the section
    const section = workspace.sections.find(s => s.id === parseInt(sectionId));
    if (!section) {
      return res.status(404).json({ error: 'Section not found' });
    }
    
    // Update section data
    if (title !== undefined) section.title = title;
    if (content !== undefined) section.content = content;
    
    // Save updated workspace
    await fs.writeFile(workspacePath, JSON.stringify(workspace, null, 2));
    
    res.json({ 
      success: true, 
      message: 'Section saved successfully',
      section: section
    });
    
  } catch (error) {
    console.error('Save error:', error);
    res.status(500).json({ 
      error: 'Failed to save section',
      message: error.message 
    });
  }
});

// Serve homepage
app.get('/', (req, res) => {
  res.sendFile(path.join(__dirname, 'public', 'index.html'));
});

// Serve workspace page
app.get('/workspace/:workspaceId', (req, res) => {
  res.sendFile(path.join(__dirname, 'public', 'workspace.html'));
});

// Start server
app.listen(PORT, () => {
  console.log(`EQUIS SAR MVP server running on http://localhost:${PORT}`);
  console.log('Upload .docx files to create workspaces');
});
