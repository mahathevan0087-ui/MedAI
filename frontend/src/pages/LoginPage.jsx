import styles from './LoginPage.module.css'

export default function LoginPage() {
  return (
    <section className={styles.loginPage}>
      <div className={styles.loginCard}>
        <span>Secure access</span>
        <h1>Sign in to MedAI+</h1>
        <p>Access patient reports, AI summaries, and clinical workflows from one secure platform.</p>
        <form className={styles.loginForm}>
          <label>
            Email
            <input type="email" placeholder="you@hospital.com" />
          </label>
          <label>
            Password
            <input type="password" placeholder="Enter your password" />
          </label>
          <button type="submit">Sign in</button>
        </form>
      </div>
    </section>
  )
}
