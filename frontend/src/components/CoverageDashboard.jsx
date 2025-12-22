import React from 'react'
import { BarChart3, CheckCircle, AlertCircle, TrendingUp } from 'lucide-react'
import './CoverageDashboard.css'

const CoverageDashboard = ({ coverage }) => {
  if (!coverage) {
    return (
      <div className="coverage-dashboard">
        <div className="dashboard-empty">
          <p>No coverage data available</p>
        </div>
      </div>
    )
  }

  const overallCoverage = coverage.overall_coverage || 0
  const standards = coverage.standards || []
  const priorityTasks = coverage.priority_tasks || []
  const missingCount = coverage.missing_evidence_count || 0

  return (
    <div className="coverage-dashboard">
      <div className="dashboard-container">
        <div className="dashboard-header">
          <h1>Coverage Dashboard</h1>
          <p>EQUIS Standards Coverage Analysis</p>
        </div>

        <div className="overview-section">
          <div className="coverage-card main">
            <div className="card-icon">
              <BarChart3 size={32} />
            </div>
            <div className="card-content">
              <h3>Overall Coverage</h3>
              <div className="coverage-percentage">
                {overallCoverage.toFixed(1)}%
              </div>
              <div className="coverage-bar-large">
                <div 
                  className="coverage-fill"
                  style={{ 
                    width: `${overallCoverage}%`,
                    background: overallCoverage > 70 ? '#10b981' : 
                               overallCoverage > 40 ? '#f59e0b' : '#ef4444'
                  }}
                ></div>
              </div>
            </div>
          </div>

          <div className="stats-grid">
            <div className="stat-card">
              <CheckCircle size={24} />
              <div>
                <div className="stat-value">
                  {standards.reduce((sum, s) => sum + s.covered_criteria, 0)}
                </div>
                <div className="stat-label">Covered Criteria</div>
              </div>
            </div>

            <div className="stat-card">
              <AlertCircle size={24} />
              <div>
                <div className="stat-value">{missingCount}</div>
                <div className="stat-label">Missing Evidence</div>
              </div>
            </div>

            <div className="stat-card">
              <TrendingUp size={24} />
              <div>
                <div className="stat-value">{standards.length}</div>
                <div className="stat-label">Total Standards</div>
              </div>
            </div>
          </div>
        </div>

        <div className="standards-section">
          <h2>Standards Breakdown</h2>
          
          <div className="standards-list">
            {standards.map((standard, index) => (
              <div key={index} className="standard-card">
                <div className="standard-header">
                  <div className="standard-info">
                    <span className="standard-number">Standard {standard.standard_number}</span>
                    <h3>{standard.standard_title}</h3>
                  </div>
                  <div 
                    className="standard-score"
                    style={{
                      color: standard.coverage_score > 70 ? '#10b981' : 
                             standard.coverage_score > 40 ? '#f59e0b' : '#ef4444'
                    }}
                  >
                    {standard.coverage_score.toFixed(0)}%
                  </div>
                </div>

                <div className="standard-progress">
                  <div 
                    className="progress-fill"
                    style={{ 
                      width: `${standard.coverage_score}%`,
                      background: standard.coverage_score > 70 ? '#10b981' : 
                                 standard.coverage_score > 40 ? '#f59e0b' : '#ef4444'
                    }}
                  ></div>
                </div>

                <div className="standard-stats">
                  <span>
                    {standard.covered_criteria} / {standard.criteria_count} criteria covered
                  </span>
                </div>

                {standard.missing_criteria.length > 0 && (
                  <div className="missing-criteria">
                    <h4>Missing Criteria:</h4>
                    <div className="criteria-tags">
                      {standard.missing_criteria.map((criterion, idx) => (
                        <span key={idx} className="criterion-tag">
                          {criterion}
                        </span>
                      ))}
                    </div>
                  </div>
                )}
              </div>
            ))}
          </div>
        </div>

        {priorityTasks.length > 0 && (
          <div className="priority-section">
            <h2>Priority Action Items</h2>
            <p>Focus on these areas to improve your SAR coverage</p>
            
            <div className="priority-list">
              {priorityTasks.map((task, index) => (
                <div key={index} className="priority-item">
                  <div className="priority-number">{index + 1}</div>
                  <p>{task}</p>
                </div>
              ))}
            </div>
          </div>
        )}

        <div className="dashboard-footer">
          <p>
            <strong>Recommendation:</strong> Focus on standards with coverage below 70% 
            and address missing criteria items with supporting evidence.
          </p>
        </div>
      </div>
    </div>
  )
}

export default CoverageDashboard
