import { useEffect, useState } from 'react'
import RiskMap from '../components/RiskMap.jsx'
import RiskPanel from '../components/RiskPanel.jsx'
import { getFloodRisk } from '../services/api.js'

function Dashboard() {
  const [riskData, setRiskData] = useState([])
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    getFloodRisk().then((data) => {
      setRiskData(data)
      setLoading(false)
    })
  }, [])

  return (
    <div className="dashboard-grid">
      <section className="map-section">
        <RiskMap points={riskData} />
      </section>
      <aside className="panel-section">
        <RiskPanel points={riskData} loading={loading} />
      </aside>
    </div>
  )
}

export default Dashboard
