import React, { useState } from 'react'
import { useDropzone } from 'react-dropzone'
import { Upload, FileText, File, CheckCircle } from 'lucide-react'
import { uploadSAR, uploadEvidence, generateDraft, getCoverage } from '../services/api'
import './Onboarding.css'

const Onboarding = ({ sessionId, onComplete }) => {
  const [sarFile, setSarFile] = useState(null)
  const [evidenceFiles, setEvidenceFiles] = useState([])
  const [uploading, setUploading] = useState(false)
  const [generating, setGenerating] = useState(false)
  const [step, setStep] = useState(1)
  const [error, setError] = useState(null)

  const onDropSAR = (acceptedFiles) => {
    if (acceptedFiles.length > 0) {
      setSarFile(acceptedFiles[0])
      setError(null)
    }
  }

  const onDropEvidence = (acceptedFiles) => {
    setEvidenceFiles(prev => [...prev, ...acceptedFiles])
    setError(null)
  }

  const { getRootProps: getSARRootProps, getInputProps: getSARInputProps, isDragActive: isSARDragActive } = useDropzone({
    onDrop: onDropSAR,
    accept: {
      'application/pdf': ['.pdf'],
      'application/vnd.openxmlformats-officedocument.wordprocessingml.document': ['.docx'],
      'application/vnd.oasis.opendocument.text': ['.odt'],
      'text/plain': ['.txt']
    },
    multiple: false
  })

  const { getRootProps: getEvidenceRootProps, getInputProps: getEvidenceInputProps, isDragActive: isEvidenceDragActive } = useDropzone({
    onDrop: onDropEvidence,
    accept: {
      'application/pdf': ['.pdf'],
      'application/vnd.openxmlformats-officedocument.wordprocessingml.document': ['.docx'],
      'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet': ['.xlsx'],
      'text/csv': ['.csv'],
      'application/vnd.openxmlformats-officedocument.presentationml.presentation': ['.pptx'],
      'image/*': ['.png', '.jpg', '.jpeg']
    },
    multiple: true
  })

  const handleUploadSAR = async () => {
    if (!sarFile) {
      setError('Please select a SAR file')
      return
    }

    setUploading(true)
    setError(null)

    try {
      await uploadSAR(sessionId, sarFile)
      setStep(2)
    } catch (err) {
      setError(err.response?.data?.detail || 'Failed to upload SAR')
    } finally {
      setUploading(false)
    }
  }

  const handleUploadEvidence = async () => {
    if (evidenceFiles.length === 0) {
      setError('Please add at least one evidence file')
      return
    }

    setUploading(true)
    setError(null)

    try {
      await uploadEvidence(sessionId, evidenceFiles)
      setStep(3)
    } catch (err) {
      setError(err.response?.data?.detail || 'Failed to upload evidence')
    } finally {
      setUploading(false)
    }
  }

  const handleGenerateDraft = async () => {
    setGenerating(true)
    setError(null)

    try {
      const draftResponse = await generateDraft(sessionId)
      const coverageResponse = await getCoverage(sessionId)
      
      onComplete(draftResponse.data.draft, coverageResponse.data)
    } catch (err) {
      setError(err.response?.data?.detail || 'Failed to generate draft')
    } finally {
      setGenerating(false)
    }
  }

  const removeEvidenceFile = (index) => {
    setEvidenceFiles(prev => prev.filter((_, i) => i !== index))
  }

  return (
    <div className="onboarding">
      <div className="onboarding-container">
        <div className="onboarding-header">
          <h1>EQUIS SAR Generator</h1>
          <p className="banner">
            Upload your previous SAR and supporting files. The app will draft a 2026 SAR 
            that mirrors your original structure — suggestions can be shown or hidden and 
            accepted inline. All files are deleted when you end the session.
          </p>
        </div>

        <div className="onboarding-steps">
          <div className={`step ${step >= 1 ? 'active' : ''} ${step > 1 ? 'completed' : ''}`}>
            <div className="step-number">{step > 1 ? <CheckCircle size={24} /> : '1'}</div>
            <div className="step-title">Upload Previous SAR</div>
          </div>
          <div className={`step ${step >= 2 ? 'active' : ''} ${step > 2 ? 'completed' : ''}`}>
            <div className="step-number">{step > 2 ? <CheckCircle size={24} /> : '2'}</div>
            <div className="step-title">Upload Evidence</div>
          </div>
          <div className={`step ${step >= 3 ? 'active' : ''}`}>
            <div className="step-number">3</div>
            <div className="step-title">Generate Draft</div>
          </div>
        </div>

        {error && (
          <div className="error-message">
            {error}
          </div>
        )}

        {step === 1 && (
          <div className="step-content">
            <h2>Step 1: Upload Your Previous SAR</h2>
            <p>Upload your 2022 SAR document (.docx, .pdf, .odt, or .txt)</p>
            
            <div 
              {...getSARRootProps()} 
              className={`dropzone ${isSARDragActive ? 'active' : ''}`}
            >
              <input {...getSARInputProps()} />
              <Upload size={48} />
              {sarFile ? (
                <div className="file-info">
                  <FileText size={24} />
                  <span>{sarFile.name}</span>
                  <span className="file-size">
                    ({(sarFile.size / 1024 / 1024).toFixed(2)} MB)
                  </span>
                </div>
              ) : (
                <p>Drag and drop your SAR file here, or click to browse</p>
              )}
            </div>

            <button 
              onClick={handleUploadSAR}
              disabled={!sarFile || uploading}
              className="btn-primary"
            >
              {uploading ? 'Uploading...' : 'Continue'}
            </button>
          </div>
        )}

        {step === 2 && (
          <div className="step-content">
            <h2>Step 2: Upload Supporting Evidence</h2>
            <p>Upload evidence files (.pdf, .docx, .xlsx, .csv, .pptx, images)</p>
            
            <div 
              {...getEvidenceRootProps()} 
              className={`dropzone ${isEvidenceDragActive ? 'active' : ''}`}
            >
              <input {...getEvidenceInputProps()} />
              <Upload size={48} />
              <p>Drag and drop evidence files here, or click to browse</p>
              <small>You can upload multiple files at once</small>
            </div>

            {evidenceFiles.length > 0 && (
              <div className="files-list">
                <h3>Uploaded Files ({evidenceFiles.length})</h3>
                {evidenceFiles.map((file, index) => (
                  <div key={index} className="file-item">
                    <File size={20} />
                    <span className="file-name">{file.name}</span>
                    <span className="file-size">
                      ({(file.size / 1024).toFixed(0)} KB)
                    </span>
                    <button 
                      onClick={() => removeEvidenceFile(index)}
                      className="btn-remove"
                    >
                      ×
                    </button>
                  </div>
                ))}
              </div>
            )}

            <div className="button-group">
              <button 
                onClick={() => setStep(1)}
                className="btn-secondary"
              >
                Back
              </button>
              <button 
                onClick={handleUploadEvidence}
                disabled={evidenceFiles.length === 0 || uploading}
                className="btn-primary"
              >
                {uploading ? 'Uploading...' : 'Continue'}
              </button>
            </div>
          </div>
        )}

        {step === 3 && (
          <div className="step-content">
            <h2>Step 3: Generate Your 2026 SAR Draft</h2>
            <p>
              The app will analyze your previous SAR and evidence files, map content to 
              EQUIS standards, and generate a draft with suggestions.
            </p>
            
            <div className="summary">
              <div className="summary-item">
                <FileText size={24} />
                <div>
                  <strong>Previous SAR</strong>
                  <p>{sarFile?.name}</p>
                </div>
              </div>
              <div className="summary-item">
                <File size={24} />
                <div>
                  <strong>Evidence Files</strong>
                  <p>{evidenceFiles.length} files uploaded</p>
                </div>
              </div>
            </div>

            {generating && (
              <div className="generating">
                <div className="spinner"></div>
                <p>Generating your SAR draft... This may take a minute.</p>
              </div>
            )}

            <div className="button-group">
              <button 
                onClick={() => setStep(2)}
                className="btn-secondary"
                disabled={generating}
              >
                Back
              </button>
              <button 
                onClick={handleGenerateDraft}
                disabled={generating}
                className="btn-primary btn-large"
              >
                {generating ? 'Generating...' : 'Generate Draft'}
              </button>
            </div>
          </div>
        )}
      </div>
    </div>
  )
}

export default Onboarding
