import styles from './Footer.module.css'

export default function Footer() {
  return (
    <footer className={styles.footer}>
      <div className={styles.container}>
        <div>
          <p className={styles.brand}>MedAI+</p>
          <p className={styles.description}>
            AI-powered medical report analysis for clinicians and health-conscious patients.
          </p>
        </div>
        <div className={styles.grid}>
          <div>
            <p className={styles.sectionTitle}>Contact</p>
            <p>support@medai.plus</p>
            <p>+1 (555) 018-2930</p>
          </div>
          <div>
            <p className={styles.sectionTitle}>Social</p>
            <a href="#">LinkedIn</a>
            <a href="#">Twitter</a>
            <a href="#">GitHub</a>
          </div>
          <div>
            <p className={styles.sectionTitle}>Office</p>
            <p>125 Health Blvd</p>
            <p>San Francisco, CA</p>
          </div>
        </div>
      </div>
      <div className={styles.copy}>© 2026 MedAI+. All rights reserved.</div>
    </footer>
  )
}
