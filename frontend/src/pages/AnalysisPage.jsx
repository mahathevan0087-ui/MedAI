import { useEffect, useState } from 'react'
import { useNavigate } from 'react-router-dom'
import styles from './AnalysisPage.module.css'

export default function AnalysisPage() {
  const [loading, setLoading] = useState(true)
  const navigate = useNavigate()

  useEffect(() => {
    const timer = setTimeout(() => {
      setLoading(false)
      navigate('/results', { replace: true })
    }, 2600)
    return () => clearTimeout(timer)
  }, [navigate])

  return (
    <section className={styles.analysisPage}>
      <div className={styles.analysisCard}>
        <div className={styles.statusPill}>AI processing</div>
        <h1>Analyzing your medical report</h1>
        <p>MedAI+ is extracting clinical values and identifying any abnormal findings.</p>
        <div className={styles.loaderWrapper}>
          <div className={styles.spinner} />
          <div className={styles.loaderText}>Analyzing with clinical AI</div>
        </div>
        <div className={styles.stepList}>
          <div>
            <strong>1.</strong>
            <span>OCR conversion</span>
          </div>
          <div>
            <strong>2.</strong>
            <span>Data normalization</span>
          </div>
          <div>
            <strong>3.</strong>
            <span>Risk scoring</span>
          </div>
        </div>
      </div>
    </section>
  )
}
