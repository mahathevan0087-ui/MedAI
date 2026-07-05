import styles from './ContactPage.module.css'

export default function ContactPage() {
  return (
    <section className={styles.contactPage}>
      <div className={styles.contactCard}>
        <span>Get in touch</span>
        <h1>Questions about MedAI+?</h1>
        <p>Reach out to our support team for assistance with report uploads, analysis results, or account setup.</p>
        <div className={styles.contactGrid}>
          <div>
            <h2>Email support</h2>
            <p>support@medai.plus</p>
          </div>
          <div>
            <h2>Phone</h2>
            <p>+1 (555) 018-2930</p>
          </div>
          <div>
            <h2>Office</h2>
            <p>125 Health Blvd, San Francisco, CA</p>
          </div>
        </div>
      </div>
    </section>
  )
}
