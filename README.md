# Flash Flood Prediction System (Hilly Regions)

Problem Statement: Ministry of Home Affairs — Flash Flood Prediction using multi-source data.

## What this does
Fuses rainfall, terrain, river-level, and soil-moisture data to generate a
flood risk score per region, shown on a live map dashboard with alerts.

## Repo structure
```
flashflood-app/
├── src/                  # Frontend (React + Vite)
│   ├── components/       # RiskMap, RiskPanel, etc.
│   ├── pages/            # Dashboard, About
│   └── services/         # api.js - talks to backend
├── backend/               # API server (FastAPI/Flask) - owner: TBD
├── ml/                    # ML model, training scripts, notebooks - owner: ML lead
└── README.md
```

## How to run the frontend
```bash
npm install
npm run dev
```
Opens at http://localhost:5173

Currently the frontend runs on **mock data** (see `src/services/api.js`,
`MOCK_MODE = true`) so the UI can be built without waiting for the backend/ML
to be ready. Once backend exposes `/flood-risk`, flip `MOCK_MODE` to `false`.

## Team split
| Module | Folder | What to build |
|---|---|---|
| Data ingestion | `backend/data/` | Scripts to fetch/simulate rainfall, river level, soil moisture, DEM data |
| Preprocessing | `backend/features/` | Clean + align data, compute engineered features |
| ML model | `ml/` | Train risk-score model, export as file backend can load |
| Backend API | `backend/` | Serve predictions via `/flood-risk` endpoint |
| Frontend | `src/` | Map dashboard, risk panel, alerts UI (this is scaffolded already) |
| Alerts | `backend/alerts/` | Trigger SMS/notification when risk > threshold |

## Contribution workflow
1. Clone this repo (don't fork unless told to)
2. Create a branch: `git checkout -b feature/<your-module-name>`
3. Work inside your assigned folder
4. Push and open a PR into `main` — team lead reviews and merges

## Next steps
- [ ] ML: decide classification vs regression, pick baseline model (RF/XGBoost)
- [ ] Backend: scaffold FastAPI app with `/flood-risk` endpoint returning ML output
- [ ] Data: source or simulate a labeled dataset for hilly-region flood events
- [ ] Frontend: connect real API once backend is ready
- [ ] Alerts: mock SMS trigger for demo
