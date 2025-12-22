"""
SAR Parser - Parse uploaded SAR documents (DOCX, PDF, ODT, TXT)
Extract structure, headings, paragraphs, tables, lists
"""

import re
from pathlib import Path
from typing import Dict, List, Any, Optional
import uuid


class SARParser:
    def __init__(self):
        self.heading_patterns = [
            r'^(\d+\.)+\s+(.+)$',  # 1.2.3 Title
            r'^([A-Z][a-z]+\s+\d+):?\s+(.+)$',  # Section 1: Title
            r'^([IVX]+)\.\s+(.+)$',  # Roman numerals
        ]
    
    def parse_sar(self, file_path: str) -> Dict[str, Any]:
        """Parse SAR file and extract structure"""
        path = Path(file_path)
        ext = path.suffix.lower()
        
        if ext == ".docx":
            return self._parse_docx(file_path)
        elif ext == ".pdf":
            return self._parse_pdf(file_path)
        elif ext == ".odt":
            return self._parse_odt(file_path)
        elif ext == ".txt":
            return self._parse_txt(file_path)
        else:
            raise ValueError(f"Unsupported file type: {ext}")
    
    def _parse_docx(self, file_path: str) -> Dict[str, Any]:
        """Parse DOCX file"""
        try:
            from docx import Document
            
            doc = Document(file_path)
            sections = []
            current_section = None
            content_buffer = []
            
            for para in doc.paragraphs:
                text = para.text.strip()
                if not text:
                    continue
                
                # Check if it's a heading
                is_heading = False
                heading_info = None
                
                # Check style-based headings
                if para.style.name.startswith('Heading'):
                    level = int(para.style.name.replace('Heading', '').strip() or "1")
                    is_heading = True
                    heading_info = self._parse_heading_text(text)
                    if heading_info:
                        heading_info['level'] = level
                else:
                    # Check pattern-based headings
                    heading_info = self._parse_heading_text(text)
                    if heading_info:
                        is_heading = True
                
                if is_heading and heading_info:
                    # Save previous section
                    if current_section:
                        current_section['content'] = '\n\n'.join(content_buffer)
                        sections.append(current_section)
                    
                    # Start new section
                    current_section = {
                        'id': str(uuid.uuid4()),
                        'number': heading_info.get('number', ''),
                        'title': heading_info.get('title', text),
                        'level': heading_info.get('level', 1),
                        'content': '',
                        'original_text': text
                    }
                    content_buffer = []
                else:
                    # Add to current section content
                    if current_section:
                        content_buffer.append(text)
                    else:
                        # Content before first heading
                        if not sections:
                            sections.append({
                                'id': str(uuid.uuid4()),
                                'number': '0',
                                'title': 'Introduction',
                                'level': 1,
                                'content': text,
                                'original_text': ''
                            })
            
            # Save last section
            if current_section:
                current_section['content'] = '\n\n'.join(content_buffer)
                sections.append(current_section)
            
            # Handle tables
            tables = []
            for table in doc.tables:
                table_data = []
                for row in table.rows:
                    row_data = [cell.text.strip() for cell in row.cells]
                    table_data.append(row_data)
                tables.append(table_data)
            
            return {
                'source_file': Path(file_path).name,
                'file_type': 'docx',
                'sections': sections,
                'tables': tables,
                'total_sections': len(sections)
            }
            
        except Exception as e:
            raise Exception(f"Error parsing DOCX: {str(e)}")
    
    def _parse_pdf(self, file_path: str) -> Dict[str, Any]:
        """Parse PDF file (with OCR fallback)"""
        try:
            import fitz  # PyMuPDF
            
            doc = fitz.open(file_path)
            sections = []
            current_section = None
            content_buffer = []
            
            for page_num, page in enumerate(doc):
                text = page.get_text()
                
                # Split into paragraphs
                paragraphs = [p.strip() for p in text.split('\n\n') if p.strip()]
                
                for para in paragraphs:
                    # Check if heading
                    heading_info = self._parse_heading_text(para)
                    
                    if heading_info:
                        # Save previous section
                        if current_section:
                            current_section['content'] = '\n\n'.join(content_buffer)
                            sections.append(current_section)
                        
                        # Start new section
                        current_section = {
                            'id': str(uuid.uuid4()),
                            'number': heading_info.get('number', ''),
                            'title': heading_info.get('title', para),
                            'level': heading_info.get('level', 1),
                            'content': '',
                            'original_text': para,
                            'page': page_num + 1
                        }
                        content_buffer = []
                    else:
                        if current_section:
                            content_buffer.append(para)
                        else:
                            # Create intro section
                            sections.append({
                                'id': str(uuid.uuid4()),
                                'number': '0',
                                'title': 'Introduction',
                                'level': 1,
                                'content': para,
                                'page': page_num + 1
                            })
            
            # Save last section
            if current_section:
                current_section['content'] = '\n\n'.join(content_buffer)
                sections.append(current_section)
            
            doc.close()
            
            return {
                'source_file': Path(file_path).name,
                'file_type': 'pdf',
                'sections': sections,
                'total_sections': len(sections)
            }
            
        except Exception as e:
            raise Exception(f"Error parsing PDF: {str(e)}")
    
    def _parse_odt(self, file_path: str) -> Dict[str, Any]:
        """Parse ODT file (simplified)"""
        # For now, convert to text and parse
        return self._parse_txt(file_path)
    
    def _parse_txt(self, file_path: str) -> Dict[str, Any]:
        """Parse plain text file"""
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        sections = []
        current_section = None
        content_buffer = []
        
        lines = content.split('\n')
        for line in lines:
            line = line.strip()
            if not line:
                continue
            
            heading_info = self._parse_heading_text(line)
            
            if heading_info:
                # Save previous section
                if current_section:
                    current_section['content'] = '\n\n'.join(content_buffer)
                    sections.append(current_section)
                
                # Start new section
                current_section = {
                    'id': str(uuid.uuid4()),
                    'number': heading_info.get('number', ''),
                    'title': heading_info.get('title', line),
                    'level': heading_info.get('level', 1),
                    'content': '',
                    'original_text': line
                }
                content_buffer = []
            else:
                if current_section:
                    content_buffer.append(line)
                else:
                    # Create intro section
                    sections.append({
                        'id': str(uuid.uuid4()),
                        'number': '0',
                        'title': 'Introduction',
                        'level': 1,
                        'content': line
                    })
        
        # Save last section
        if current_section:
            current_section['content'] = '\n\n'.join(content_buffer)
            sections.append(current_section)
        
        return {
            'source_file': Path(file_path).name,
            'file_type': 'txt',
            'sections': sections,
            'total_sections': len(sections)
        }
    
    def _parse_heading_text(self, text: str) -> Optional[Dict[str, Any]]:
        """Parse heading text to extract number and title"""
        for pattern in self.heading_patterns:
            match = re.match(pattern, text)
            if match:
                groups = match.groups()
                if len(groups) >= 2:
                    number = groups[0].strip()
                    title = groups[1].strip()
                    
                    # Estimate level from number
                    level = number.count('.') + 1 if '.' in number else 1
                    
                    return {
                        'number': number,
                        'title': title,
                        'level': level
                    }
        
        # Check if text looks like a heading (short, title case, etc.)
        if len(text) < 100 and text[0].isupper() and not text.endswith('.'):
            return {
                'number': '',
                'title': text,
                'level': 1
            }
        
        return None
