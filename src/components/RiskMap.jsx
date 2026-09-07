import { MapContainer, TileLayer, CircleMarker, Popup, useMap } from 'react-leaflet'
import { useEffect } from 'react'
import L from 'leaflet'
import 'leaflet/dist/leaflet.css'

const DEFAULT_CENTER = [22.9734, 78.6569] // fallback: center of India

function riskColor(score) {
  if (score >= 70) return '#d32f2f' // high risk - red
  if (score >= 40) return '#f9a825' // medium risk - amber
  return '#2e7d32' // low risk - green
}

// Automatically zooms/pans the map so every region marker is visible,
// instead of relying on a fixed center+zoom that can cut off far regions.
function FitBounds({ points }) {
  const map = useMap()

  useEffect(() => {
    if (points.length === 0) return
    const bounds = L.latLngBounds(points.map((p) => [p.lat, p.lng]))
    map.fitBounds(bounds, { padding: [40, 40] })
  }, [points, map])

  return null
}

function Legend() {
  return (
    <div className="map-legend">
      <div className="legend-title">Risk Level</div>
      <div className="legend-item"><span className="dot" style={{ background: '#d32f2f' }} /> High (70+)</div>
      <div className="legend-item"><span className="dot" style={{ background: '#f9a825' }} /> Medium (40-69)</div>
      <div className="legend-item"><span className="dot" style={{ background: '#2e7d32' }} /> Low (0-39)</div>
    </div>
  )
}

function RiskMap({ points }) {
  return (
    <div style={{ position: 'relative', height: '100%', width: '100%' }}>
      <MapContainer center={DEFAULT_CENTER} zoom={5} style={{ height: '100%', width: '100%' }}>
        <TileLayer
          attribution='&copy; OpenStreetMap contributors'
          url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
        />
        <FitBounds points={points} />
        {points.map((p) => (
          <CircleMarker
            key={p.id}
            center={[p.lat, p.lng]}
            radius={12}
            pathOptions={{ color: riskColor(p.riskScore), fillColor: riskColor(p.riskScore), fillOpacity: 0.8, weight: 2 }}
          >
            <Popup>
              <strong>{p.name}</strong><br />
              Risk score: {p.riskScore}<br />
              Rainfall: {p.rainfallMm} mm
            </Popup>
          </CircleMarker>
        ))}
      </MapContainer>
      <Legend />
    </div>
  )
}

export default RiskMap
