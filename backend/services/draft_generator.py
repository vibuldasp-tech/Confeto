"""
Draft Generator - Generate 2026 SAR draft with suggestions
Identify carry-forward text and generate new recommendations
Create inline suggestions with EQUIS clause citations
"""

from typing import Dict, List, Any
import uuid
import re


class DraftGenerator:
    def __init__(self):
        pass
    
    def generate_draft(
        self,
        parsed_sar: Dict[str, Any],
        mapping_results: List[Dict[str, Any]],
        equis_index: Dict[str, Any],
        evidence_files: List[Dict[str, Any]]
    ) -> Dict[str, Any]:
        """Generate 2026 SAR draft with suggestions"""
        
        draft_sections = []
        
        # Create mapping lookup
        mapping_lookup = {m['section_id']: m for m in mapping_results}
        
        for section in parsed_sar['sections']:
            section_id = section['id']
            mapping = mapping_lookup.get(section_id, {})
            
            # Generate draft section
            draft_section = self._generate_section_draft(
                section,
                mapping,
                equis_index,
                evidence_files
            )
            
            draft_sections.append(draft_section)
        
        return {
            'title': '2026 EQUIS Self-Assessment Report',
            'sections': draft_sections,
            'metadata': {
                'source_file': parsed_sar.get('source_file'),
                'generation_date': 'Generated',
                'total_sections': len(draft_sections)
            }
        }
    
    def _generate_section_draft(
        self,
        section: Dict[str, Any],
        mapping: Dict[str, Any],
        equis_index: Dict[str, Any],
        evidence_files: List[Dict[str, Any]]
    ) -> Dict[str, Any]:
        """Generate draft for a single section"""
        
        original_content = section.get('content', '')
        matched_criteria = mapping.get('matched_criteria', [])
        evidence_matches = mapping.get('evidence_matches', [])
        coverage_score = mapping.get('coverage_score', 0)
        
        # Determine if we can carry forward text
        carry_forward_score = self._calculate_carry_forward_score(
            original_content,
            matched_criteria
        )
        
        # Generate suggestions
        suggestions = []
        
        if carry_forward_score > 0.7:
            # High confidence carry-forward with minor edits
            suggestions.extend(
                self._generate_refinement_suggestions(
                    original_content,
                    matched_criteria,
                    equis_index
                )
            )
        else:
            # Low confidence - suggest major rewrite
            suggestions.extend(
                self._generate_rewrite_suggestions(
                    section,
                    matched_criteria,
                    equis_index
                )
            )
        
        # Add evidence citation suggestions
        suggestions.extend(
            self._generate_evidence_suggestions(
                original_content,
                evidence_matches
            )
        )
        
        # Generate evidence links
        evidence_links = self._create_evidence_links(evidence_matches)
        
        # Determine final clean text (default = original with light improvements)
        clean_text = self._apply_default_improvements(
            original_content,
            matched_criteria
        )
        
        return {
            'id': section['id'],
            'number': section.get('number', ''),
            'title': section.get('title', ''),
            'level': section.get('level', 1),
            'content': clean_text,
            'original_content': original_content,
            'suggestions': suggestions,
            'evidence_links': evidence_links,
            'coverage_score': coverage_score,
            'carry_forward_score': carry_forward_score,
            'equis_criteria': [c['criterion'] for c in matched_criteria],
            'gaps': mapping.get('gaps', [])
        }
    
    def _calculate_carry_forward_score(
        self,
        content: str,
        matched_criteria: List[Dict[str, Any]]
    ) -> float:
        """Calculate how suitable the content is for carrying forward"""
        
        if not content or len(content) < 50:
            return 0.0
        
        # Check criteria match quality
        if not matched_criteria:
            return 0.3
        
        best_match = matched_criteria[0].get('similarity', 0) if matched_criteria else 0
        
        # Check for dated content (2022, 2021, etc.)
        has_old_dates = bool(re.search(r'202[0-2]', content))
        
        # Check for evidence references
        has_evidence = bool(re.search(r'(see|refer|appendix|exhibit)', content, re.IGNORECASE))
        
        score = best_match
        if has_old_dates:
            score *= 0.8  # Penalize old dates
        if has_evidence:
            score *= 1.1  # Reward evidence references
        
        return min(1.0, score)
    
    def _generate_refinement_suggestions(
        self,
        content: str,
        matched_criteria: List[Dict[str, Any]],
        equis_index: Dict[str, Any]
    ) -> List[Dict[str, Any]]:
        """Generate suggestions for refining existing text"""
        
        suggestions = []
        
        # Suggest updating dates
        old_dates = re.finditer(r'(202[0-2])', content)
        for match in old_dates:
            suggestions.append({
                'id': str(uuid.uuid4()),
                'type': 'replacement',
                'position': match.start(),
                'original_text': match.group(0),
                'suggested_text': '2025',
                'rationale': 'Update year to current assessment period',
                'confidence': 0.95,
                'accepted': None
            })
        
        # Suggest adding EQUIS criterion reference
        if matched_criteria:
            top_criterion = matched_criteria[0]
            suggestion_text = f"\n\nThis addresses EQUIS Standard {top_criterion['criterion']}: \"{top_criterion['text']}\""
            
            suggestions.append({
                'id': str(uuid.uuid4()),
                'type': 'insertion',
                'position': len(content),
                'original_text': None,
                'suggested_text': suggestion_text,
                'rationale': f"Explicitly link to EQUIS criterion {top_criterion['criterion']}",
                'equis_clause': top_criterion['text'],
                'equis_clause_number': top_criterion['criterion'],
                'confidence': 0.85,
                'accepted': None
            })
        
        return suggestions
    
    def _generate_rewrite_suggestions(
        self,
        section: Dict[str, Any],
        matched_criteria: List[Dict[str, Any]],
        equis_index: Dict[str, Any]
    ) -> List[Dict[str, Any]]:
        """Generate suggestions for rewriting section"""
        
        suggestions = []
        
        if matched_criteria:
            # Suggest comprehensive rewrite aligned with criteria
            top_criteria = matched_criteria[:3]
            
            suggested_text = f"[SUGGESTED REWRITE]\n\n"
            suggested_text += f"This section addresses "
            suggested_text += ", ".join([f"EQUIS Standard {c['criterion']}" for c in top_criteria])
            suggested_text += ".\n\n"
            suggested_text += "Consider including:\n"
            
            for criterion in top_criteria:
                suggested_text += f"- {criterion['text']}\n"
            
            suggestions.append({
                'id': str(uuid.uuid4()),
                'type': 'replacement',
                'position': 0,
                'original_text': section.get('content', ''),
                'suggested_text': suggested_text,
                'rationale': 'Section requires significant revision to better align with EQUIS criteria',
                'equis_clause': top_criteria[0]['text'] if top_criteria else None,
                'equis_clause_number': top_criteria[0]['criterion'] if top_criteria else None,
                'confidence': 0.6,
                'accepted': None
            })
        else:
            # No criteria matched
            suggestions.append({
                'id': str(uuid.uuid4()),
                'type': 'replacement',
                'position': 0,
                'original_text': section.get('content', ''),
                'suggested_text': '[EVIDENCE MISSING / UNCERTAIN]\n\nThis section does not clearly map to any EQUIS criteria. Consider:\n1. Reviewing EQUIS Standards to identify relevant criteria\n2. Restructuring content to address specific standards\n3. Providing evidence and examples',
                'rationale': 'No EQUIS criteria match found',
                'confidence': 0.5,
                'accepted': None
            })
        
        return suggestions
    
    def _generate_evidence_suggestions(
        self,
        content: str,
        evidence_matches: List[Dict[str, Any]]
    ) -> List[Dict[str, Any]]:
        """Generate suggestions for adding evidence citations"""
        
        suggestions = []
        
        if not evidence_matches:
            return suggestions
        
        # Suggest adding footnote for top evidence match
        for evidence in evidence_matches[:2]:  # Top 2
            if evidence['confidence'] > 0.6:
                citation_text = f" [See: {evidence['filename']}]"
                
                suggestions.append({
                    'id': str(uuid.uuid4()),
                    'type': 'insertion',
                    'position': len(content),
                    'original_text': None,
                    'suggested_text': citation_text,
                    'rationale': f"Add citation to supporting evidence (confidence: {evidence['confidence']:.0%})",
                    'confidence': evidence['confidence'],
                    'accepted': None,
                    'evidence_file': evidence['filename']
                })
        
        return suggestions
    
    def _create_evidence_links(self, evidence_matches: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Create structured evidence links"""
        
        links = []
        
        for evidence in evidence_matches:
            if evidence['confidence'] > 0.4:
                excerpt = evidence['excerpts'][0] if evidence.get('excerpts') else ''
                
                links.append({
                    'file_id': evidence['file_id'],
                    'filename': evidence['filename'],
                    'excerpt': excerpt[:200] + '...' if len(excerpt) > 200 else excerpt,
                    'confidence': evidence['confidence']
                })
        
        return links
    
    def _apply_default_improvements(
        self,
        content: str,
        matched_criteria: List[Dict[str, Any]]
    ) -> str:
        """Apply minimal improvements to create clean default text"""
        
        # Update obvious dates
        improved = re.sub(r'\b202[0-2]\b', '2025', content)
        
        # Add criterion reference if high confidence
        if matched_criteria and matched_criteria[0].get('similarity', 0) > 0.8:
            top = matched_criteria[0]
            improved += f"\n\n[Note: This section aligns with EQUIS Standard {top['criterion']}]"
        
        return improved
    
    def calculate_coverage(
        self,
        mapping_results: List[Dict[str, Any]],
        equis_index: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Calculate overall coverage dashboard"""
        
        # Get all criteria
        all_criteria = set()
        covered_criteria = set()
        
        for standard in equis_index.get('standards', []):
            for criterion in standard.get('criteria', []):
                all_criteria.add(criterion['full_number'])
        
        # Check coverage
        for mapping in mapping_results:
            for match in mapping.get('matched_criteria', []):
                if match.get('similarity', 0) > 0.5:
                    covered_criteria.add(match['criterion'])
        
        overall_coverage = len(covered_criteria) / len(all_criteria) * 100 if all_criteria else 0
        
        # Per-standard coverage
        standard_coverage = []
        for standard in equis_index.get('standards', []):
            standard_criteria = set(c['full_number'] for c in standard['criteria'])
            standard_covered = standard_criteria & covered_criteria
            
            coverage_score = len(standard_covered) / len(standard_criteria) * 100 if standard_criteria else 0
            
            missing = list(standard_criteria - covered_criteria)
            
            standard_coverage.append({
                'standard_number': standard['number'],
                'standard_title': standard['title'],
                'coverage_score': coverage_score,
                'criteria_count': len(standard_criteria),
                'covered_criteria': len(standard_covered),
                'missing_criteria': missing
            })
        
        # Priority tasks
        priority_tasks = []
        for std in standard_coverage:
            if std['coverage_score'] < 70:
                priority_tasks.append(
                    f"Improve coverage for Standard {std['standard_number']}: {std['standard_title']} "
                    f"(currently {std['coverage_score']:.0f}%)"
                )
        
        return {
            'overall_coverage': overall_coverage,
            'standards': standard_coverage,
            'missing_evidence_count': len(all_criteria - covered_criteria),
            'priority_tasks': priority_tasks
        }
