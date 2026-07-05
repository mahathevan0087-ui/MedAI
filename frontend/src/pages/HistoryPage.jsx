import styles from './HistoryPage.module.css'

const reports = [
  { title: 'Cardiac Panel', date: 'June 14, 2026', status: 'Reviewed' },
  { title: 'Annual Wellness Report', date: 'May 9, 2026', status: 'Pending' },
  { title: 'Metabolic Health Scan', date: 'April 3, 2026', status: 'Reviewed' },
]

export default function HistoryPage() {
  return (
    <section className={styles.historyPage}>
      <div className={styles.pageHeader}>
        <span>Report History</span>
        <h1>All past analyses for your care team.</h1>
      </div>
      <div className={styles.reportGrid}>
        {reports.map((report) => (
          <article key={report.title} className={styles.reportCard}>
            <div className={styles.reportHeader}>
              <h2>{report.title}</h2>
              <span className={report.status === 'Reviewed' ? styles.reviewed : styles.pending}>{report.status}</span>
            </div>
            <p>{report.date}</p>
            <div className={styles.reportFooter}>
              <button type="button">View report</button>
              <span>Summary available</span>
            </div>
          </article>
        ))}
      </div>
    </section>
  )
}
