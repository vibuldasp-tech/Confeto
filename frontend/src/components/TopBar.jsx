import React, { useState } from 'react'
import { FileText, BarChart3, Download, Trash2, HelpCircle, Home } from 'lucide-react'
import { exportDOCX, deleteSession } from '../services/api'
import './TopBar.css'

const TopBar = ({ onViewChange, currentView, sessionId, onNewSession }) => {
  const [exporting, setExporting] = useState(false)
  const [showExportOptions, setShowExportOptions] = useState(false)
  const [exportOptions, setExportOptions] = useState({
    include_suggestions: false,
    include_footnotes: true,
    include_annex: false
  })

  const handleExport = async () => {
    setExporting(true)
    try {
      const response = await exportDOCX(sessionId, exportOptions)
      
      // Create download link
      const url = window.URL.createObjectURL(new Blob([response.data]))
      const link = document.createElement('a')
      link.href = url
      link.setAttribute('download', 'EQUIS_SAR_2026_Draft.docx')
      document.body.appendChild(link)
      link.click()
      link.remove()
      
      setShowExportOptions(false)
    } catch (error) {
      console.error('Export failed:', error)
      alert('Failed to export document')
    } finally {
      setExporting(false)
    }
  }

  const handleDeleteSession = async () => {
    if (window.confirm('Are you sure you want to delete this session? All files and generated content will be removed.')) {
      try {
        await deleteSession(sessionId)
        onNewSession()
      } catch (error) {
        console.error('Failed to delete session:', error)
      }
    }
  }

  return (
    <div className="top-bar">
      <div className="top-bar-left">
        <div className="logo">
          <FileText size={24} />
          <span>EQUIS SAR Generator</span>
        </div>
      </div>

      <div className="top-bar-center">
        <button 
          className={`nav-btn ${currentView === 'editor' ? 'active' : ''}`}
          onClick={() => onViewChange('editor')}
        >
          <FileText size={18} />
          <span>Editor</span>
        </button>
        <button 
          className={`nav-btn ${currentView === 'dashboard' ? 'active' : ''}`}
          onClick={() => onViewChange('dashboard')}
        >
          <BarChart3 size={18} />
          <span>Coverage</span>
        </button>
      </div>

      <div className="top-bar-right">
        <button 
          className="icon-btn"
          onClick={() => setShowExportOptions(!showExportOptions)}
          title="Export to DOCX"
        >
          <Download size={18} />
        </button>
        
        <button 
          className="icon-btn"
          onClick={handleDeleteSession}
          title="Delete Session"
        >
          <Trash2 size={18} />
        </button>
        
        <button 
          className="icon-btn"
          onClick={() => alert('Help: This tool helps you generate an EQUIS SAR draft. Upload your previous SAR and evidence, then edit the generated draft with AI suggestions.')}
          title="Help"
        >
          <HelpCircle size={18} />
        </button>
      </div>

      {showExportOptions && (
        <div className="export-modal">
          <div className="export-modal-content">
            <h3>Export Options</h3>
            
            <label className="checkbox-label">
              <input
                type="checkbox"
                checked={exportOptions.include_footnotes}
                onChange={(e) => setExportOptions({
                  ...exportOptions,
                  include_footnotes: e.target.checked
                })}
              />
              <span>Include evidence footnotes</span>
            </label>
            
            <label className="checkbox-label">
              <input
                type="checkbox"
                checked={exportOptions.include_suggestions}
                onChange={(e) => setExportOptions({
                  ...exportOptions,
                  include_suggestions: e.target.checked
                })}
              />
              <span>Include inline suggestions</span>
            </label>
            
            <label className="checkbox-label">
              <input
                type="checkbox"
                checked={exportOptions.include_annex}
                onChange={(e) => setExportOptions({
                  ...exportOptions,
                  include_annex: e.target.checked
                })}
              />
              <span>Include suggestions annex</span>
            </label>
            
            <div className="modal-actions">
              <button 
                className="btn-secondary"
                onClick={() => setShowExportOptions(false)}
              >
                Cancel
              </button>
              <button 
                className="btn-primary"
                onClick={handleExport}
                disabled={exporting}
              >
                {exporting ? 'Exporting...' : 'Export'}
              </button>
            </div>
          </div>
          <div 
            className="modal-overlay"
            onClick={() => setShowExportOptions(false)}
          ></div>
        </div>
      )}
    </div>
  )
}

export default TopBar
