import React, { useState, useEffect } from 'react'
import Onboarding from './components/Onboarding'
import MainEditor from './components/MainEditor'
import CoverageDashboard from './components/CoverageDashboard'
import TopBar from './components/TopBar'
import { createSession } from './services/api'
import './styles/App.css'

function App() {
  const [sessionId, setSessionId] = useState(null)
  const [currentView, setCurrentView] = useState('onboarding')
  const [draft, setDraft] = useState(null)
  const [coverage, setCoverage] = useState(null)
  const [loading, setLoading] = useState(false)

  useEffect(() => {
    // Create session on mount
    initializeSession()
  }, [])

  const initializeSession = async () => {
    try {
      const response = await createSession()
      setSessionId(response.data.session_id)
    } catch (error) {
      console.error('Failed to create session:', error)
    }
  }

  const handleOnboardingComplete = (generatedDraft, coverageData) => {
    setDraft(generatedDraft)
    setCoverage(coverageData)
    setCurrentView('editor')
  }

  const handleViewChange = (view) => {
    setCurrentView(view)
  }

  const handleNewSession = () => {
    // Reset and create new session
    setCurrentView('onboarding')
    setDraft(null)
    setCoverage(null)
    initializeSession()
  }

  return (
    <div className="app">
      {sessionId && currentView !== 'onboarding' && (
        <TopBar 
          onViewChange={handleViewChange}
          currentView={currentView}
          sessionId={sessionId}
          onNewSession={handleNewSession}
        />
      )}
      
      <div className="app-content">
        {currentView === 'onboarding' && (
          <Onboarding 
            sessionId={sessionId}
            onComplete={handleOnboardingComplete}
          />
        )}
        
        {currentView === 'editor' && draft && (
          <MainEditor 
            sessionId={sessionId}
            draft={draft}
            onDraftUpdate={setDraft}
          />
        )}
        
        {currentView === 'dashboard' && coverage && (
          <CoverageDashboard 
            coverage={coverage}
          />
        )}
      </div>
    </div>
  )
}

export default App
