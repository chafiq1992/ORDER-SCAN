# Order‑Scanner App

A full‑stack rewrite of the original Google‑Apps‑Script barcode scanner.

* **Backend** — FastAPI + async SQLAlchemy, containerised for Google Cloud Run.
* **Database** — Supabase (PostgreSQL).
* **Frontend** — React 18 + Vite + Tailwind + Framer Motion.
* **Optional** — still appends rows to Google Sheets if env‑vars are supplied.

## Local dev (backend)

```bash
python -m venv venv && source venv/bin/activate
pip install -r backend/requirements.txt
uvicorn app.main:app --reload --app-dir backend/app
```

## Local dev (frontend)

```bash
cd frontend
npm install
npm run dev
```

## Build & Deploy

1. Push this repo to GitHub  
2. Run:

```bash
gcloud builds submit --tag gcr.io/$PROJECT/order-scanner .
gcloud run deploy order-scanner --image gcr.io/$PROJECT/order-scanner --platform managed --region europe-west1 --allow-unauthenticated       --update-env-vars SUPABASE_DB_URL=postgresql+asyncpg://user:pass@host:5432/db,SHOPIFY_STORES_JSON='[{"name":"irrakids",...}]'
```

## Environment variables

| Variable | Required | Description |
|----------|----------|-------------|
| `SUPABASE_DB_URL` | ✅ | Postgres URL (`postgresql+asyncpg://...`) |
| `SHOPIFY_STORES_JSON` | ✅ | JSON array of stores with keys `name,api_key,password,domain` |
| `GOOGLE_SHEET_ID` | ❌ | Sheet key if you still want sheet logging |
| `GOOGLE_SERVICE_ACCOUNT_JSON` | ❌ | Base64‑encoded service‑account key |
