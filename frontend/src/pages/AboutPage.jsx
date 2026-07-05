import styles from './AboutPage.module.css'

export default function AboutPage() {
  return (
    <section className={styles.aboutPage}>
      <div className={styles.heroSplit}>
        <div>
          <span>About MedAI+</span>
          <h1>Transforming medical reports into clinical clarity with AI.</h1>
          <p>
            MedAI+ combines secure OCR, domain-aware AI analysis, and a clinician-focused dashboard to empower better decision-making.
          </p>
        </div>
        <div className={styles.aboutCard}>
          <h2>Designed for healthcare teams</h2>
          <p>
            The platform streamlines review of lab reports, radiology notes, and clinical summaries while highlighting the most relevant findings.
          </p>
          <div className={styles.aboutStats}>
            <div>
              <strong>500+</strong>
              <span>medical users</span>
            </div>
            <div>
              <strong>99%</strong>
              <span>uptime guarantee</span>
            </div>
          </div>
        </div>
      </div>

      <div className={styles.featureList}>
        <article>
          <h3>Secure and compliant</h3>
          <p>Patient data is protected with encryption and strict access controls for clinical environments.</p>
        </article>
        <article>
          <h3>Data-driven recommendations</h3>
          <p>AI highlights risk signals and suggests follow-up monitoring priorities.</p>
        </article>
        <article>
          <h3>Fast report triage</h3>
          <p>Spend less time reading documents and more time acting on insights that matter.</p>
        </article>
      </div>
    </section>
  )
}
