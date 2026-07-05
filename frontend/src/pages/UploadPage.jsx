import { useState } from 'react'
import styles from './UploadPage.module.css'

const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://127.0.0.1:5000'

const ALLOWED_TYPES = [
  'image/jpeg',
  'image/png',
  'image/bmp',
  'image/tiff',
  'application/pdf',
]

function renderListItem(item, idx) {
  // Guard: if backend somehow sends an object, stringify it gracefully
  if (typeof item === 'object' && item !== null) {
    return <li key={idx}>{Object.entries(item).map(([k, v]) => `${k}: ${v}`).join(' · ')}</li>
  }
  return <li key={idx}>{String(item)}</li>
}

function UploadPage() {
  const [file, setFile] = useState(null)
  const [isUploading, setIsUploading] = useState(false)
  const [uploadStage, setUploadStage] = useState('') // 'ocr' | 'ai' | ''
  const [error, setError] = useState('')
  const [analysisResult, setAnalysisResult] = useState(null)

  const handleFileChange = (e) => {
    const selected = e.target.files[0]
    if (!selected) return

    if (!ALLOWED_TYPES.includes(selected.type)) {
      setError('Unsupported file type. Please upload a PDF, JPG, or PNG.')
      setFile(null)
      return
    }
    setError('')
    setFile(selected)
  }

  const uploadFile = async () => {
    if (!file) {
      setError('Please select a file first.')
      return
    }

    const formData = new FormData()
    formData.append('file', file)

    setIsUploading(true)
    setUploadStage('ocr')
    setError('')
    setAnalysisResult(null)

    // Simulate OCR → AI stage labels for better UX
    const aiTimer = setTimeout(() => setUploadStage('ai'), 4000)

    try {
      const response = await fetch(`${API_BASE_URL}/upload`, {
        method: 'POST',
        body: formData,
      })

      clearTimeout(aiTimer)

      const data = await response.json()

      if (!response.ok) {
        throw new Error(data.message || data.error || 'Upload failed')
      }

      setAnalysisResult(data)
      setFile(null)
    } catch (err) {
      setError(err.message || 'Upload failed. Is the backend running?')
    } finally {
      clearTimeout(aiTimer)
      setIsUploading(false)
      setUploadStage('')
    }
  }

  return (
    <div className={styles.container}>
      <div className={styles.uploadSection}>
        <h1>Upload Medical Report</h1>
        <p>Upload a medical report (PDF, JPG, PNG) for AI-powered analysis</p>

        <div className={styles.uploadBox}>
          <input
            type="file"
            id="fileInput"
            accept=".pdf,.jpg,.jpeg,.png,.bmp,.tiff"
            onChange={handleFileChange}
            disabled={isUploading}
            className={styles.fileInput}
          />
          <p className={styles.fileName}>
            {file ? `✅ Selected: ${file.name}` : 'No file selected'}
          </p>
        </div>

        <button
          onClick={uploadFile}
          disabled={isUploading || !file}
          className={styles.uploadButton}
        >
          {isUploading ? (
            <>
              <span className={styles.spinner} />
              {uploadStage === 'ai' ? 'Analysing with AI...' : 'Extracting text...'}
            </>
          ) : (
            'Upload & Analyse'
          )}
        </button>

        {error && <div className={styles.error}>{error}</div>}
      </div>

      {isUploading && (
        <div className={styles.loadingSection}>
          <div className={styles.loadingContainer}>
            <div className={styles.loadingSpinner} />
            {uploadStage === 'ai' ? (
              <>
                <p>🤖 Gemini AI is analysing your report...</p>
                <p className={styles.subText}>This may take 10–30 seconds</p>
              </>
            ) : (
              <>
                <p>📄 Extracting text from your report...</p>
                <p className={styles.subText}>Running OCR on the document</p>
              </>
            )}
          </div>
        </div>
      )}

      {analysisResult && !isUploading && (
        <div className={styles.resultsSection}>
          <div className={styles.resultsHeader}>
            <h2>Medical Report Analysis</h2>
            <p className={styles.filename}>📁 File: {analysisResult.filename}</p>
          </div>

          <div className={styles.analysisGrid}>
            {/* Summary */}
            <div className={styles.card}>
              <div className={styles.cardHeader}>
                <h3>Summary</h3>
                <span className={styles.icon}>📋</span>
              </div>
              <p className={styles.summary}>
                {analysisResult.analysis?.summary || 'No summary available.'}
              </p>
            </div>

            {/* Abnormal Values */}
            <div className={styles.card}>
              <div className={styles.cardHeader}>
                <h3>Abnormal Values</h3>
                <span className={styles.icon}>⚠️</span>
              </div>
              {analysisResult.analysis?.abnormal_values?.length > 0 ? (
                <ul className={styles.list}>
                  {analysisResult.analysis.abnormal_values.map(renderListItem)}
                </ul>
              ) : (
                <p className={styles.noData}>No abnormal values detected</p>
              )}
            </div>

            {/* Possible Conditions */}
            <div className={styles.card}>
              <div className={styles.cardHeader}>
                <h3>Possible Conditions</h3>
                <span className={styles.icon}>🩺</span>
              </div>
              {analysisResult.analysis?.possible_conditions?.length > 0 ? (
                <ul className={styles.list}>
                  {analysisResult.analysis.possible_conditions.map(renderListItem)}
                </ul>
              ) : (
                <p className={styles.noData}>No conditions identified</p>
              )}
            </div>

            {/* Recommendations */}
            <div className={styles.card}>
              <div className={styles.cardHeader}>
                <h3>Recommendations</h3>
                <span className={styles.icon}>✅</span>
              </div>
              {analysisResult.analysis?.recommendations?.length > 0 ? (
                <ul className={styles.list}>
                  {analysisResult.analysis.recommendations.map(renderListItem)}
                </ul>
              ) : (
                <p className={styles.noData}>No recommendations</p>
              )}
            </div>
          </div>

          {/* OCR text (collapsible) */}
          {analysisResult.ocr_text && (
            <details className={styles.ocrDetails}>
              <summary>📝 View extracted OCR text</summary>
              <pre className={styles.ocrText}>{analysisResult.ocr_text}</pre>
            </details>
          )}

          <button
            onClick={() => {
              setAnalysisResult(null)
              setFile(null)
            }}
            className={styles.resetButton}
          >
            Upload Another Report
          </button>
        </div>
      )}
    </div>
  )
}

export default UploadPage
