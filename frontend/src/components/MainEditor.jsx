import React, { useState } from 'react'
import SectionNavigator from './SectionNavigator'
import RichTextEditor from './RichTextEditor'
import EvidencePanel from './EvidencePanel'
import './MainEditor.css'

const MainEditor = ({ sessionId, draft, onDraftUpdate }) => {
  const [selectedSection, setSelectedSection] = useState(
    draft?.sections?.[0] || null
  )
  const [showSuggestions, setShowSuggestions] = useState(false)

  const handleSectionSelect = (section) => {
    setSelectedSection(section)
  }

  const handleSectionUpdate = (updatedSection) => {
    // Update the section in draft
    const updatedDraft = {
      ...draft,
      sections: draft.sections.map(s => 
        s.id === updatedSection.id ? updatedSection : s
      )
    }
    onDraftUpdate(updatedDraft)
    setSelectedSection(updatedSection)
  }

  if (!draft || !draft.sections || draft.sections.length === 0) {
    return (
      <div className="main-editor">
        <div className="no-content">
          <p>No draft available</p>
        </div>
      </div>
    )
  }

  return (
    <div className="main-editor">
      <SectionNavigator 
        sections={draft.sections}
        selectedSection={selectedSection}
        onSectionSelect={handleSectionSelect}
      />
      
      <div className="editor-main">
        {selectedSection ? (
          <>
            <div className="editor-header">
              <div className="section-info">
                <h2>{selectedSection.number} {selectedSection.title}</h2>
                <div className="section-meta">
                  <span className="coverage-badge" 
                    style={{
                      background: selectedSection.coverage_score > 70 ? '#d1fae5' : 
                                 selectedSection.coverage_score > 40 ? '#fef3c7' : '#fee2e2',
                      color: selectedSection.coverage_score > 70 ? '#065f46' : 
                             selectedSection.coverage_score > 40 ? '#92400e' : '#991b1b'
                    }}
                  >
                    Coverage: {selectedSection.coverage_score.toFixed(0)}%
                  </span>
                  {selectedSection.equis_criteria.length > 0 && (
                    <span className="criteria-badge">
                      EQUIS: {selectedSection.equis_criteria.join(', ')}
                    </span>
                  )}
                </div>
              </div>
              
              <label className="toggle-suggestions">
                <input
                  type="checkbox"
                  checked={showSuggestions}
                  onChange={(e) => setShowSuggestions(e.target.checked)}
                />
                <span>Show Suggestions</span>
              </label>
            </div>
            
            <RichTextEditor 
              section={selectedSection}
              showSuggestions={showSuggestions}
              onSectionUpdate={handleSectionUpdate}
              sessionId={sessionId}
            />
          </>
        ) : (
          <div className="no-section-selected">
            <p>Select a section from the navigator</p>
          </div>
        )}
      </div>
      
      <EvidencePanel 
        section={selectedSection}
      />
    </div>
  )
}

export default MainEditor
