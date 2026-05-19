# SkillRadar Backend — Setup Guide

## 1. Run Supabase Schema

Go to https://supabase.com/dashboard → your `skillradar` project → SQL Editor → paste contents of `backend/data/schema.sql` → Run.

You should see "Success" and 7 tables created.

## 2. Install Python Dependencies

Make sure you have **Python 3.10+** installed.

```bash
cd backend
python -m venv venv
# Windows:
venv\Scripts\activate
# Mac/Linux:
source venv/bin/activate

pip install -r requirements.txt
```

If Prophet fails to install (it's heavy), skip it — the forecaster has a linear fallback.

## 3. Install spaCy English Model

```bash
python -m spacy download en_core_web_sm
```

## 4. Run the Server

```bash
python app.py
```

You should see:
```
Starting SkillRadar API on port 5000
  Adzuna: configured
  Remotive: configured
  JSearch: configured
  Database: connected
```

## 5. Test It

Open another terminal:

```bash
# Health check
curl http://localhost:5000/api/health

# Real-time job search
curl "http://localhost:5000/api/jobs/search?q=python&location=Pune"

# Top skills (will be empty until you ingest data)
curl http://localhost:5000/api/skills/top
```

## 6. Populate the Database (First Time)

```bash
curl -X POST http://localhost:5000/api/jobs/ingest \
  -H "Content-Type: application/json" \
  -d '{"queries": ["python developer", "data scientist", "react developer", "java developer", "devops engineer"], "location": "India"}'
```

This fetches ~150 jobs, extracts skills, saves to Supabase. Takes ~30 seconds.

Now all the analytics endpoints have data:

```bash
curl http://localhost:5000/api/skills/top
curl http://localhost:5000/api/skills/trending
curl -X POST http://localhost:5000/api/clusters/refresh
curl http://localhost:5000/api/clusters
```

## Endpoints Available

| Method | Path | Purpose |
|---|---|---|
| GET | `/api/health` | Server status |
| GET | `/api/jobs/search` | Live search across 3 APIs |
| GET | `/api/jobs/saved-data` | Browse jobs from database |
| POST | `/api/jobs/ingest` | Fetch fresh jobs into DB |
| GET | `/api/skills/top` | Most frequent skills |
| GET | `/api/skills/trending` | Skills with high growth |
| GET | `/api/skills/emerging` | New skills appearing |
| GET | `/api/skills/declining` | Skills losing demand |
| GET | `/api/skills/categories` | Category distribution |
| POST | `/api/skills/extract` | Extract skills from a JD/resume |
| GET | `/api/clusters` | K-Means role clusters |
| POST | `/api/clusters/refresh` | Re-run clustering |
| GET | `/api/forecast/<skill>` | Prophet forecast for one skill |
| GET | `/api/forecast/top/all` | Forecasts for top 8 skills |
| POST | `/api/users/register` | Create/login user |
| GET | `/api/users/<id>/saved` | User's saved jobs |
| POST | `/api/users/<id>/save` | Save a job |
| DELETE | `/api/users/<id>/save/<job_id>` | Remove saved job |

## Troubleshooting

**"Database not configured"** → Your `.env` file isn't being read. Make sure you're in the `backend/` folder when running `python app.py`.

**"Connection refused" from Supabase** → Check your Supabase project is "active" (not paused). Free tier pauses after 7 days of inactivity — just unpause it in dashboard.

**Adzuna 401 / 403** → Wrong key or you exceeded 250/month free quota.

**JSearch quota exceeded** → 200/month free. The cache will save you.
