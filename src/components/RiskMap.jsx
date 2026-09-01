import { MapContainer, TileLayer, CircleMarker, Popup } from 'react-leaflet'
import 'leaflet/dist/leaflet.css'

// Default center: roughly central India hilly belt — change to your target region
const DEFAULT_CENTER = [30.0668, 79.0193] // e.g. Uttarakhand hills

function riskColor(score) {
  if (score >= 70) return '#d32f2f' // high risk - red
  if (score >= 40) return '#f9a825' // medium risk - amber
  return '#2e7d32' // low risk - green
}

function RiskMap({ points }) {
  return (
    <MapContainer center={DEFAULT_CENTER} zoom={8} style={{ height: '100%', width: '100%' }}>
      <TileLayer
        attribution='&copy; OpenStreetMap contributors'
        url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
      />
      {points.map((p) => (
        <CircleMarker
          key={p.id}
          center={[p.lat, p.lng]}
          radius={10}
          pathOptions={{ color: riskColor(p.riskScore), fillColor: riskColor(p.riskScore), fillOpacity: 0.7 }}
        >
          <Popup>
            <strong>{p.name}</strong><br />
            Risk score: {p.riskScore}<br />
            Rainfall: {p.rainfallMm} mm
          </Popup>
        </CircleMarker>
      ))}
    </MapContainer>
  )
}

export default RiskMap
