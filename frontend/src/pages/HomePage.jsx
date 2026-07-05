import { useMemo } from 'react'
import { Link } from 'react-router-dom'
import styles from './HomePage.module.css'

const features = [
  {
    title: 'Smart OCR Extraction',
    description: 'Extract clinical text from reports and images with high accuracy.',
    icon: '🧠',
  },
  {
    title: 'AI Risk Detection',
    description: 'Highlight abnormal values and generate risk assessments instantly.',
    icon: '🩺',
  },
  {
    title: 'Report Summaries',
    description: 'Receive concise, clinician-ready summaries in seconds.',
    icon: '📄',
  },
  {
    title: 'Secure Cloud Storage',
    description: 'Encrypted report history and safe patient data handling.',
    icon: '🔒',
  },
  {
    title: 'Interactive Dashboard',
    description: 'Visualize metrics, trends, and insights with confidence.',
    icon: '📊',
  },
  {
    title: 'Fast Case Collaboration',
    description: 'Share findings quickly with care teams and medical staff.',
    icon: '🤝',
  },
]

const workflow = [
  { label: 'Upload', detail: 'Submit PDFs or scans.' },
  { label: 'OCR', detail: 'Convert text from medical documents.' },
  { label: 'AI Analysis', detail: 'Detect anomalies and patterns.' },
  { label: 'Summary', detail: 'Review a clinician-ready brief.' },
]

export default function HomePage() {
  const featureCards = useMemo(
    () =>
      features.map((feature, index) => (
        <article key={index} className={styles.card}>
          <div className={styles.cardAccent}>{feature.icon}</div>
          <h3>{feature.title}</h3>
          <p>{feature.description}</p>
        </article>
      )),
    [],
  )

  return (
    <>
      <section className={styles.heroSection}>
        <div className={styles.heroCopy}>
          <span className={styles.tag}>AI-Powered Medical Intelligence</span>
          <h1>MedAI+ makes report analysis faster, safer, and more predictive.</h1>
          <p>Upload medical reports, identify abnormal findings, and get actionable summaries powered by advanced AI.</p>
          <div className={styles.heroActions}>
            <Link to="/upload" className={styles.primaryButton}>Upload Report</Link>
            <a href="#features" className={styles.secondaryButton}>Explore features</a>
          </div>
          <div className={styles.heroStats}>
            <div>
              <strong>98%</strong>
              <span>OCR accuracy</span>
            </div>
            <div>
              <strong>24/7</strong>
              <span>Clinical insights</span>
            </div>
            <div>
              <strong>500+</strong>
              <span>Trusted hospitals</span>
            </div>
          </div>
        </div>
        <div className={styles.heroVisual}>
          <div className={styles.visualGradient} />
          <div className={styles.heroCard}>
            <div className={styles.heroTag}>Medical report analysis</div>
            <h2>AI reads your reports. You make decisions faster.</h2>
            <div className={styles.heroMetrics}>
              <div>
                <p>Heart rate</p>
                <strong>82 bpm</strong>
              </div>
              <div>
                <p>Blood sugar</p>
                <strong>5.8 mmol/L</strong>
              </div>
            </div>
          </div>
        </div>
      </section>

      <section id="features" className={styles.featuresSection}>
        <div className={styles.sectionHeader}>
          <span>Features</span>
          <h2>Clinical intelligence built for modern care teams.</h2>
        </div>
        <div className={styles.featureGrid}>{featureCards}</div>
      </section>

      <section id="workflow" className={styles.workflowSection}>
        <div className={styles.sectionHeader}>
          <span>How It Works</span>
          <h2>From upload to summary in four seamless steps.</h2>
        </div>
        <div className={styles.workflowGrid}>
          {workflow.map((step, index) => (
            <article key={step.label} className={styles.workflowCard}>
              <div className={styles.workflowStep}>{index + 1}</div>
              <h3>{step.label}</h3>
              <p>{step.detail}</p>
            </article>
          ))}
        </div>
      </section>
    </>
  )
}
