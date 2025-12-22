"""
Semantic Mapper - Map SAR sections to EQUIS criteria
Use semantic similarity to match content with standards
Find supporting evidence for each section
"""

from typing import Dict, List, Any
import uuid
import re


class SemanticMapper:
    def __init__(self):
        self.model = None
        self._init_model()
    
    def _init_model(self):
        """Initialize semantic similarity model"""
        try:
            from sentence_transformers import SentenceTransformer, util
            self.model = SentenceTransformer('all-MiniLM-L6-v2')
            self.util = util
        except Exception as e:
            print(f"Warning: Could not load semantic model: {e}")
            self.model = None
    
    def map_sections_to_criteria(
        self, 
        sections: List[Dict[str, Any]], 
        equis_index: Dict[str, Any],
        evidence_files: List[Dict[str, Any]]
    ) -> List[Dict[str, Any]]:
        """Map each SAR section to EQUIS criteria"""
        
        results = []
        
        # Get all criteria texts for embedding
        criteria_texts = []
        criteria_refs = []
        
        for standard in equis_index.get('standards', []):
            for criterion in standard.get('criteria', []):
                criteria_texts.append(criterion['text'])
                criteria_refs.append({
                    'standard': standard['number'],
                    'criterion': criterion['full_number'],
                    'text': criterion['text'],
                    'page': criterion.get('page', 1)
                })
        
        # Encode criteria if model available
        if self.model and criteria_texts:
            criteria_embeddings = self.model.encode(criteria_texts, convert_to_tensor=True)
        else:
            criteria_embeddings = None
        
        # Map each section
        for section in sections:
            section_text = f"{section.get('title', '')} {section.get('content', '')}"
            
            if self.model and criteria_embeddings is not None:
                # Semantic matching
                section_embedding = self.model.encode(section_text, convert_to_tensor=True)
                similarities = self.util.cos_sim(section_embedding, criteria_embeddings)[0]
                
                # Get top matches
                top_matches = []
                for idx, score in enumerate(similarities):
                    if score > 0.3:  # Threshold
                        top_matches.append({
                            'criterion': criteria_refs[idx]['criterion'],
                            'text': criteria_refs[idx]['text'],
                            'standard': criteria_refs[idx]['standard'],
                            'page': criteria_refs[idx]['page'],
                            'similarity': float(score)
                        })
                
                # Sort by similarity
                top_matches.sort(key=lambda x: x['similarity'], reverse=True)
                matched_criteria = top_matches[:5]  # Top 5
                
                # Calculate coverage score
                if matched_criteria:
                    coverage_score = min(100, matched_criteria[0]['similarity'] * 100)
                else:
                    coverage_score = 0
            else:
                # Fallback: keyword matching
                matched_criteria = self._keyword_match(section_text, criteria_refs)
                coverage_score = 50 if matched_criteria else 0
            
            # Find evidence matches
            evidence_matches = self._find_evidence_matches(
                section_text,
                evidence_files
            )
            
            results.append({
                'section_id': section.get('id'),
                'section_title': section.get('title'),
                'matched_criteria': matched_criteria,
                'coverage_score': coverage_score,
                'evidence_matches': evidence_matches,
                'gaps': self._identify_gaps(matched_criteria, section_text)
            })
        
        return results
    
    def _keyword_match(self, text: str, criteria_refs: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Fallback keyword-based matching"""
        text_lower = text.lower()
        matches = []
        
        for criterion in criteria_refs:
            criterion_text = criterion['text'].lower()
            
            # Simple keyword overlap
            text_words = set(re.findall(r'\w+', text_lower))
            criterion_words = set(re.findall(r'\w+', criterion_text))
            
            overlap = len(text_words & criterion_words)
            if overlap > 3:
                matches.append({
                    'criterion': criterion['criterion'],
                    'text': criterion['text'],
                    'standard': criterion['standard'],
                    'page': criterion['page'],
                    'similarity': min(1.0, overlap / 10)
                })
        
        matches.sort(key=lambda x: x['similarity'], reverse=True)
        return matches[:5]
    
    def _find_evidence_matches(
        self, 
        section_text: str, 
        evidence_files: List[Dict[str, Any]]
    ) -> List[Dict[str, Any]]:
        """Find evidence files that support this section"""
        matches = []
        
        if not evidence_files:
            return matches
        
        section_lower = section_text.lower()
        
        # Extract key phrases from section (simple approach)
        key_phrases = self._extract_key_phrases(section_text)
        
        for evidence in evidence_files:
            parsed = evidence.get('parsed', {})
            evidence_text = parsed.get('text', '').lower()
            
            if not evidence_text:
                continue
            
            # Check for key phrase matches
            match_score = 0
            matched_excerpts = []
            
            for phrase in key_phrases:
                if phrase.lower() in evidence_text:
                    match_score += 1
                    
                    # Extract context
                    idx = evidence_text.find(phrase.lower())
                    context_start = max(0, idx - 50)
                    context_end = min(len(evidence_text), idx + len(phrase) + 50)
                    context = evidence_text[context_start:context_end]
                    
                    matched_excerpts.append(context)
            
            if match_score > 0:
                confidence = min(1.0, match_score / len(key_phrases))
                
                matches.append({
                    'file_id': evidence.get('file_id'),
                    'filename': evidence.get('filename'),
                    'confidence': confidence,
                    'match_count': match_score,
                    'excerpts': matched_excerpts[:3]  # Top 3 excerpts
                })
        
        # Sort by confidence
        matches.sort(key=lambda x: x['confidence'], reverse=True)
        return matches[:10]  # Top 10 evidence files
    
    def _extract_key_phrases(self, text: str, max_phrases: int = 10) -> List[str]:
        """Extract key phrases from text (simple noun phrase extraction)"""
        # Simple approach: extract capitalized phrases and common academic terms
        phrases = []
        
        # Find capitalized phrases
        capitalized = re.findall(r'[A-Z][a-z]+(?:\s+[A-Z][a-z]+)*', text)
        phrases.extend(capitalized)
        
        # Find quoted text
        quoted = re.findall(r'"([^"]+)"', text)
        phrases.extend(quoted)
        
        # Extract words longer than 6 characters (likely domain-specific)
        long_words = re.findall(r'\b\w{7,}\b', text)
        phrases.extend(long_words)
        
        # Remove duplicates and limit
        phrases = list(set(phrases))[:max_phrases]
        
        return phrases
    
    def _identify_gaps(self, matched_criteria: List[Dict[str, Any]], section_text: str) -> List[str]:
        """Identify gaps or missing elements"""
        gaps = []
        
        if not matched_criteria:
            gaps.append("No EQUIS criteria matched. Section may need significant revision.")
        elif len(matched_criteria) < 2:
            gaps.append("Limited criteria coverage. Consider addressing additional standards.")
        
        # Check for evidence references
        if not re.search(r'(see|refer|appendix|exhibit|table|figure)', section_text, re.IGNORECASE):
            gaps.append("No evidence references found. Consider adding citations to supporting documents.")
        
        # Check for data/metrics
        if not re.search(r'(\d+%|\d+\.\d+|table|chart|data)', section_text, re.IGNORECASE):
            gaps.append("Limited quantitative data. Consider adding metrics or statistics.")
        
        return gaps
