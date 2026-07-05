import styles from './ResultsPage.module.css'

const testResults = [
  { name: 'LDL Cholesterol', value: '146 mg/dL', status: 'High' },
  { name: 'Blood Glucose', value: '112 mg/dL', status: 'Pre-diabetes' },
  { name: 'White Blood Cells', value: '8.9 x10³/µL', status: 'Normal' },
  { name: 'Hemoglobin A1c', value: '6.1%', status: 'Elevated' },
]

export default function ResultsPage() {
  return (
    <section className={styles.resultsPage}>
      <div className={styles.resultsGrid}>
        <div className={styles.summaryCard}>
          <span className={styles.overline}>AI Insights</span>
          <h1>Analysis results ready for review</h1>
          <p>Get a quick view of your key labs, abnormal markers, and overall health risk profile.</p>
          <div className={styles.metricRow}>
            <div>
              <p>Risk score</p>
              <strong>78 / 100</strong>
            </div>
            <div>
              <p>Condition</p>
              <strong>Moderate risk</strong>
            </div>
          </div>
        </div>

        <div className={styles.tableCard}>
          <div className={styles.tableHeader}>
            <h2>Test values</h2>
            <span>Automatically flagged abnormalities</span>
          </div>
          <div className={styles.tableBody}>
            {testResults.map((result) => (
              <div key={result.name} className={styles.tableRow}>
                <p>{result.name}</p>
                <strong>{result.value}</strong>
                <span className={result.status === 'Normal' ? styles.tagNormal : styles.tagAlert}>
                  {result.status}
                </span>
              </div>
            ))}
          </div>
        </div>
      </div>

      <div className={styles.dashBoardGrid}>
        <div className={styles.riskCard}>
          <span className={styles.overline}>Health Risk</span>
          <h2>Patient risk estimate</h2>
          <div className={styles.riskMeter}>
            <div className={styles.riskFill} />
            <strong>78%</strong>
          </div>
          <p>Clinical AI indicates an elevated risk for cardiovascular events based on lab patterns.</p>
        </div>

        <div className={styles.analysisSummary}>
          <span className={styles.overline}>AI-generated summary</span>
          <h2>Clinical summary</h2>
          <p>
            The report indicates elevated LDL cholesterol and mild glucose elevation with normal white blood cell counts.
            Continue monitoring metabolic markers and consider dietary adjustments to reduce cardiovascular risk.
          </p>
          <div className={styles.summaryBullets}>
            <p>• Review lipid panel and monitor lifestyle changes.</p>
            <p>• Evaluate glucose regulation and schedule follow-up.</p>
            <p>• Confirm findings with clinician for personalized care.</p>
          </div>
        </div>
      </div>
    </section>
  )
}
