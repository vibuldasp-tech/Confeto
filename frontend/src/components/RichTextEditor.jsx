import React, { useState } from 'react'
import { Check, X, Info } from 'lucide-react'
import { updateSection } from '../services/api'
import './RichTextEditor.css'

const RichTextEditor = ({ section, showSuggestions, onSectionUpdate, sessionId }) => {
  const [content, setContent] = useState(section.content)
  const [saving, setSaving] = useState(false)
  const [suggestions, setSuggestions] = useState(section.suggestions || [])

  const handleContentChange = (e) => {
    setContent(e.target.value)
  }

  const handleSave = async () => {
    setSaving(true)
    try {
      await updateSection(sessionId, section.id, {
        content,
        accepted_suggestions: suggestions.filter(s => s.accepted).map(s => s.id),
        rejected_suggestions: suggestions.filter(s => s.accepted === false).map(s => s.id)
      })
      
      onSectionUpdate({
        ...section,
        content,
        suggestions
      })
    } catch (error) {
      console.error('Failed to save:', error)
      alert('Failed to save changes')
    } finally {
      setSaving(false)
    }
  }

  const handleAcceptSuggestion = (suggestionId) => {
    const suggestion = suggestions.find(s => s.id === suggestionId)
    if (!suggestion) return

    // Update content based on suggestion type
    let newContent = content

    if (suggestion.type === 'replacement' && suggestion.original_text) {
      newContent = newContent.replace(suggestion.original_text, suggestion.suggested_text)
    } else if (suggestion.type === 'insertion') {
      newContent = newContent + '\n\n' + suggestion.suggested_text
    }

    setContent(newContent)

    // Mark suggestion as accepted
    setSuggestions(suggestions.map(s => 
      s.id === suggestionId ? { ...s, accepted: true } : s
    ))
  }

  const handleRejectSuggestion = (suggestionId) => {
    setSuggestions(suggestions.map(s => 
      s.id === suggestionId ? { ...s, accepted: false } : s
    ))
  }

  const pendingSuggestions = suggestions.filter(s => s.accepted === null || s.accepted === undefined)
  const acceptedCount = suggestions.filter(s => s.accepted === true).length
  const rejectedCount = suggestions.filter(s => s.accepted === false).length

  return (
    <div className="rich-text-editor">
      <div className="editor-content">
        <textarea
          className="content-textarea"
          value={content}
          onChange={handleContentChange}
          placeholder="Section content..."
        />
        
        <div className="editor-actions">
          <button 
            className="btn-save"
            onClick={handleSave}
            disabled={saving}
          >
            {saving ? 'Saving...' : 'Save Changes'}
          </button>
          <span className="save-status">
            {acceptedCount > 0 && <span className="status-accepted">{acceptedCount} accepted</span>}
            {rejectedCount > 0 && <span className="status-rejected">{rejectedCount} rejected</span>}
          </span>
        </div>
      </div>

      {showSuggestions && (
        <div className="suggestions-panel">
          <div className="suggestions-header">
            <h3>AI Suggestions</h3>
            <span className="suggestions-count">{pendingSuggestions.length} pending</span>
          </div>

          {section.gaps && section.gaps.length > 0 && (
            <div className="gaps-section">
              <h4>Identified Gaps</h4>
              {section.gaps.map((gap, index) => (
                <div key={index} className="gap-item">
                  <Info size={16} />
                  <span>{gap}</span>
                </div>
              ))}
            </div>
          )}

          <div className="suggestions-list">
            {suggestions.length === 0 ? (
              <p className="no-suggestions">No suggestions for this section</p>
            ) : (
              suggestions.map((suggestion) => (
                <div 
                  key={suggestion.id} 
                  className={`suggestion-item ${
                    suggestion.accepted === true ? 'accepted' : 
                    suggestion.accepted === false ? 'rejected' : ''
                  }`}
                >
                  <div className="suggestion-header">
                    <span className={`suggestion-type ${suggestion.type}`}>
                      {suggestion.type}
                    </span>
                    <span className="suggestion-confidence">
                      {(suggestion.confidence * 100).toFixed(0)}% confidence
                    </span>
                  </div>

                  {suggestion.original_text && (
                    <div className="suggestion-original">
                      <strong>Original:</strong>
                      <p>{suggestion.original_text.substring(0, 100)}...</p>
                    </div>
                  )}

                  <div className="suggestion-text">
                    <strong>Suggested:</strong>
                    <p>{suggestion.suggested_text}</p>
                  </div>

                  <div className="suggestion-rationale">
                    <Info size={14} />
                    <span>{suggestion.rationale}</span>
                  </div>

                  {suggestion.equis_clause && (
                    <div className="equis-clause">
                      <strong>EQUIS {suggestion.equis_clause_number}:</strong>
                      <p>{suggestion.equis_clause}</p>
                    </div>
                  )}

                  {suggestion.accepted === null || suggestion.accepted === undefined ? (
                    <div className="suggestion-actions">
                      <button 
                        className="btn-accept"
                        onClick={() => handleAcceptSuggestion(suggestion.id)}
                      >
                        <Check size={16} />
                        Accept
                      </button>
                      <button 
                        className="btn-reject"
                        onClick={() => handleRejectSuggestion(suggestion.id)}
                      >
                        <X size={16} />
                        Reject
                      </button>
                    </div>
                  ) : (
                    <div className="suggestion-status">
                      {suggestion.accepted ? (
                        <span className="status-accepted">✓ Accepted</span>
                      ) : (
                        <span className="status-rejected">✗ Rejected</span>
                      )}
                    </div>
                  )}
                </div>
              ))
            )}
          </div>
        </div>
      )}
    </div>
  )
}

export default RichTextEditor
