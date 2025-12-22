import React from 'react'
import { File, AlertCircle } from 'lucide-react'
import './EvidencePanel.css'

const EvidencePanel = ({ section }) => {
  if (!section) {
    return (
      <div className="evidence-panel">
        <div className="panel-empty">
          <p>Select a section to view evidence</p>
        </div>
      </div>
    )
  }

  const evidenceLinks = section.evidence_links || []
  const highConfidence = evidenceLinks.filter(e => e.confidence > 0.7)
  const mediumConfidence = evidenceLinks.filter(e => e.confidence > 0.4 && e.confidence <= 0.7)
  const lowConfidence = evidenceLinks.filter(e => e.confidence <= 0.4)

  return (
    <div className="evidence-panel">
      <div className="panel-header">
        <h3>Supporting Evidence</h3>
        <span className="evidence-count">{evidenceLinks.length}</span>
      </div>

      <div className="panel-content">
        {evidenceLinks.length === 0 ? (
          <div className="no-evidence">
            <AlertCircle size={48} />
            <p>No evidence linked to this section</p>
            <small>Upload evidence files during onboarding to enable automatic linking</small>
          </div>
        ) : (
          <>
            {highConfidence.length > 0 && (
              <div className="evidence-group">
                <h4 className="group-title high">High Confidence</h4>
                {highConfidence.map((evidence, index) => (
                  <div key={index} className="evidence-item">
                    <div className="evidence-header">
                      <File size={16} />
                      <span className="evidence-filename">{evidence.filename}</span>
                    </div>
                    <div className="confidence-bar">
                      <div 
                        className="confidence-fill high"
                        style={{ width: `${evidence.confidence * 100}%` }}
                      ></div>
                    </div>
                    {evidence.excerpt && (
                      <p className="evidence-excerpt">{evidence.excerpt}</p>
                    )}
                    <button className="btn-cite">Insert Citation</button>
                  </div>
                ))}
              </div>
            )}

            {mediumConfidence.length > 0 && (
              <div className="evidence-group">
                <h4 className="group-title medium">Medium Confidence</h4>
                {mediumConfidence.map((evidence, index) => (
                  <div key={index} className="evidence-item">
                    <div className="evidence-header">
                      <File size={16} />
                      <span className="evidence-filename">{evidence.filename}</span>
                    </div>
                    <div className="confidence-bar">
                      <div 
                        className="confidence-fill medium"
                        style={{ width: `${evidence.confidence * 100}%` }}
                      ></div>
                    </div>
                    {evidence.excerpt && (
                      <p className="evidence-excerpt">{evidence.excerpt}</p>
                    )}
                    <button className="btn-cite">Insert Citation</button>
                  </div>
                ))}
              </div>
            )}

            {lowConfidence.length > 0 && (
              <div className="evidence-group">
                <h4 className="group-title low">Low Confidence</h4>
                {lowConfidence.map((evidence, index) => (
                  <div key={index} className="evidence-item">
                    <div className="evidence-header">
                      <File size={16} />
                      <span className="evidence-filename">{evidence.filename}</span>
                    </div>
                    <div className="confidence-bar">
                      <div 
                        className="confidence-fill low"
                        style={{ width: `${evidence.confidence * 100}%` }}
                      ></div>
                    </div>
                    <button className="btn-cite">Insert Citation</button>
                  </div>
                ))}
              </div>
            )}
          </>
        )}
      </div>
    </div>
  )
}

export default EvidencePanel
