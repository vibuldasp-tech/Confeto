import React from 'react'
import { ChevronRight } from 'lucide-react'
import './SectionNavigator.css'

const SectionNavigator = ({ sections, selectedSection, onSectionSelect }) => {
  return (
    <div className="section-navigator">
      <div className="navigator-header">
        <h3>Sections</h3>
        <span className="section-count">{sections.length}</span>
      </div>
      
      <div className="sections-list">
        {sections.map((section) => (
          <div
            key={section.id}
            className={`section-item ${selectedSection?.id === section.id ? 'active' : ''}`}
            onClick={() => onSectionSelect(section)}
            style={{ paddingLeft: `${section.level * 12 + 12}px` }}
          >
            <div className="section-item-content">
              <span className="section-number">{section.number}</span>
              <span className="section-title">{section.title}</span>
            </div>
            
            <div className="section-indicators">
              {section.suggestions && section.suggestions.length > 0 && (
                <span 
                  className="suggestion-indicator"
                  title={`${section.suggestions.length} suggestions`}
                >
                  {section.suggestions.length}
                </span>
              )}
              
              <div 
                className="coverage-indicator"
                style={{
                  background: section.coverage_score > 70 ? '#10b981' : 
                             section.coverage_score > 40 ? '#f59e0b' : '#ef4444'
                }}
                title={`Coverage: ${section.coverage_score.toFixed(0)}%`}
              ></div>
            </div>
            
            {selectedSection?.id === section.id && (
              <ChevronRight size={16} className="active-indicator" />
            )}
          </div>
        ))}
      </div>
    </div>
  )
}

export default SectionNavigator
