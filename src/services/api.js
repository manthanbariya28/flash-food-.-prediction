import axios from 'axios'

const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000'

// Mock data so frontend team can build the UI before the ML/backend is ready.
// Once the backend module (see /backend) exposes a real /flood-risk endpoint,
// swap MOCK_MODE to false.
const MOCK_MODE = false

const MOCK_DATA = [
  { id: 1, name: 'Region A - Nainital', lat: 29.3919, lng: 79.4542, riskScore: 82, rainfallMm: 120 },
  { id: 2, name: 'Region B - Shimla', lat: 31.1048, lng: 77.1734, riskScore: 55, rainfallMm: 60 },
  { id: 3, name: 'Region C - Munnar', lat: 10.0889, lng: 77.0595, riskScore: 30, rainfallMm: 20 },
  { id: 4, name: 'Region D - Gangtok', lat: 27.3389, lng: 88.6065, riskScore: 74, rainfallMm: 95 },
]

export async function getFloodRisk() {
  if (MOCK_MODE) {
    return new Promise((resolve) => setTimeout(() => resolve(MOCK_DATA), 400))
  }
  const res = await axios.get(`${API_BASE_URL}/flood-risk`)
  return res.data
}
