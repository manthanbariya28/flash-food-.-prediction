function RiskPanel({ points, loading }) {
  if (loading) return <p>Loading risk data...</p>

  const sorted = [...points].sort((a, b) => b.riskScore - a.riskScore)

  return (
    <div className="risk-panel">
      <h2>Regions by risk</h2>
      <ul>
        {sorted.map((p) => (
          <li key={p.id} className="risk-item">
            <span className="risk-name">{p.name}</span>
            <span className="risk-score">{p.riskScore}</span>
          </li>
        ))}
      </ul>
    </div>
  )
}

export default RiskPanel
