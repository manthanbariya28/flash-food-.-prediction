import { useEffect, useState } from 'react'
import RiskMap from '../components/RiskMap.jsx'
import RiskPanel from '../components/RiskPanel.jsx'
import { getFloodRisk } from '../services/api.js'

const ALERT_THRESHOLD = 70

function Dashboard() {
  const [riskData, setRiskData] = useState([])
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    getFloodRisk().then((data) => {
      setRiskData(data)
      setLoading(false)
    })
  }, [])

  const highRiskRegions = riskData.filter((p) => p.riskScore >= ALERT_THRESHOLD)

  return (
    <div className="dashboard-wrapper">
      {highRiskRegions.length > 0 && (
        <div className="alert-banner">
          🚨 High flood risk detected: {highRiskRegions.map((r) => r.name).join(', ')}
        </div>
      )}
      <div className="dashboard-grid">
        <section className="map-section">
          <RiskMap points={riskData} />
        </section>
        <aside className="panel-section">
          <RiskPanel points={riskData} loading={loading} />
        </aside>
      </div>
    </div>
  )
}

export default Dashboard
