import axios from 'axios'

const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000'

const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
})

// Session endpoints
export const createSession = () => {
  return api.post('/api/session/create')
}

export const deleteSession = (sessionId) => {
  return api.delete(`/api/session/${sessionId}`)
}

// Upload endpoints
export const uploadSAR = (sessionId, file) => {
  const formData = new FormData()
  formData.append('file', file)
  
  return api.post(`/api/session/${sessionId}/upload-sar`, formData, {
    headers: {
      'Content-Type': 'multipart/form-data',
    },
  })
}

export const uploadEvidence = (sessionId, files) => {
  const formData = new FormData()
  files.forEach(file => {
    formData.append('files', file)
  })
  
  return api.post(`/api/session/${sessionId}/upload-evidence`, formData, {
    headers: {
      'Content-Type': 'multipart/form-data',
    },
  })
}

// Draft endpoints
export const generateDraft = (sessionId) => {
  return api.post(`/api/session/${sessionId}/generate-draft`)
}

export const getDraft = (sessionId) => {
  return api.get(`/api/session/${sessionId}/draft`)
}

export const updateSection = (sessionId, sectionId, data) => {
  return api.put(`/api/session/${sessionId}/section/${sectionId}`, data)
}

// Coverage endpoint
export const getCoverage = (sessionId) => {
  return api.get(`/api/session/${sessionId}/coverage`)
}

// Export endpoint
export const exportDOCX = (sessionId, options = {}) => {
  const params = new URLSearchParams()
  if (options.include_suggestions) params.append('include_suggestions', 'true')
  if (options.include_footnotes !== false) params.append('include_footnotes', 'true')
  if (options.include_annex) params.append('include_annex', 'true')
  
  return api.post(`/api/session/${sessionId}/export?${params.toString()}`, {}, {
    responseType: 'blob'
  })
}

export default api
