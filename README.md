# SkillRadar

> Real-time job market intelligence platform that analyzes thousands of live job postings to identify trending skills, cluster similar roles, forecast future demand, and provide AI-powered career insights.

![Status](https://img.shields.io/badge/status-active-success.svg)
![Backend](https://img.shields.io/badge/backend-Flask-blue.svg)
![Frontend](https://img.shields.io/badge/frontend-React-61dafb.svg)
![ML](https://img.shields.io/badge/ml-scikit--learn-orange.svg)
![AI](https://img.shields.io/badge/ai-Groq%20LLM-purple.svg)

---

## What Is SkillRadar?

SkillRadar continuously pulls fresh job postings from **four major job boards** (Adzuna, Remotive, JSearch via RapidAPI, and Jooble), runs NLP on every posting to extract skills, clusters similar roles using K-Means, forecasts skill demand using time-series modeling, and offers AI-powered resume analysis and chat — all in one platform.

It's built for students, job seekers, and career advisors who need to know *what employers actually want right now* — backed by live data, not last year's blog posts.

---

## Features

### 🔍 Real-Time Job Search
- Live aggregation across 4 job sources in parallel
- Smart cache-first search with auto top-up from APIs
- Auto-complete suggestions powered by 130+ role templates + DB job titles
- Save jobs for later, filter by remote/global

### 🧠 NLP Skill Extraction
- Custom taxonomy of **214 skills** across **17 categories**
- 540 pattern variations (handles JS/JavaScript, ML/Machine Learning, etc.)
- Extracts skills from raw job descriptions automatically
- Confidence-scored, context-aware

### 📈 Trend Analysis
- Top skills ranked by demand
- Trending skills (rising rapidly)
- Emerging skills (new in market)
- Declining skills (losing relevance)
- Week-over-week and month-over-month growth

### 🎯 Role Clustering
- TF-IDF vectorization of skill sets
- K-Means clustering with elbow method
- Cluster labeling using top frequent skills
- Visualized as interactive role groups

### 🔮 Demand Forecasting
- Time-series prediction per skill
- Prophet model with linear regression fallback
- 90-day forecast with weekly seasonality
- Synthetic baseline augmentation for new skills

### 🤖 AI Features
- **Resume Analyzer**: Upload PDF resume → AI extracts skills, experience, target roles
- **Job Matching**: Live jobs ranked by Jaccard similarity to your resume
- **Skill Gap Detection**: Shows what's missing for your target roles
- **Learning Resources**: Curated courses, tutorials, docs for each missing skill
- **AI Tailor**: Groq Llama 3.1 generates resume tailoring suggestions for specific jobs
- **AI Chat (RAG)**: Ask anything about the job market — answers grounded in real DB data

### 🎨 Modern UI
- Animated radar visualization (signature element)
- Light/dark themes with smooth transitions
- Glassmorphism cards, mesh gradients, scroll-reveal animations
- Frosted-glass navbar, animated number counters
- Fully responsive

---

## Tech Stack

### Backend
- **Flask** — REST API framework
- **PostgreSQL** (via Supabase) — primary database
- **scikit-learn** — K-Means clustering, TF-IDF
- **Prophet** + linear regression fallback — time-series forecasting
- **spaCy** — NLP pipeline
- **Groq Llama 3.1 70B** — AI features (RAG architecture)
- **pypdf** — PDF resume parsing
- **ThreadPoolExecutor** — parallel API calls

### Frontend
- **React 18** + **Vite** — fast modern build
- **Tailwind CSS** — utility-first styling
- **Framer Motion** — animations
- **Recharts** — data visualization
- **Axios** — API calls
- **React Router** — routing
- **Lucide React** — icons

### Data Sources
- **Adzuna API** — Indian job market focus
- **Remotive API** — remote tech jobs globally
- **JSearch (RapidAPI)** — LinkedIn / Indeed / Glassdoor aggregator
- **Jooble API** — global aggregator (70+ countries)

---

## Project Structure

```
skillradar/
├── backend/
│   ├── app.py                    # Flask app + 22 REST endpoints
│   ├── config.py                 # Environment config
│   ├── requirements.txt
│   ├── .env.example              # Template (real .env is gitignored)
│   ├── services/                 # Job API clients + aggregator
│   │   ├── adzuna_client.py
│   │   ├── remotive_client.py
│   │   ├── jsearch_client.py
│   │   ├── jooble_client.py
│   │   ├── job_aggregator.py
│   │   └── job_model.py
│   ├── nlp/                      # NLP & skill extraction
│   │   ├── skill_taxonomy.py     # 214 skills, 17 categories
│   │   ├── extractor.py
│   │   └── trend_analyzer.py
│   ├── ml/                       # Machine learning
│   │   ├── clusterer.py          # K-Means + TF-IDF
│   │   └── forecaster.py         # Prophet / linear fallback
│   ├── ai/                       # AI features
│   │   ├── resume_parser.py
│   │   ├── job_matcher.py
│   │   ├── groq_client.py
│   │   ├── context_builder.py    # RAG context
│   │   └── learning_resources.py # Curated learning links
│   ├── data/
│   │   ├── db.py                 # Database layer
│   │   └── schema.sql            # 7 tables
│   └── utils/cache.py
│
├── frontend/
│   ├── index.html
│   ├── package.json
│   ├── vite.config.js
│   ├── tailwind.config.js
│   └── src/
│       ├── App.jsx
│       ├── main.jsx
│       ├── styles.css            # Premium styles + animations
│       ├── pages/
│       │   ├── Landing.jsx       # Hero + animated radar
│       │   ├── JobSearch.jsx
│       │   ├── SkillsAnalytics.jsx
│       │   ├── RoleExplorer.jsx
│       │   ├── Forecast.jsx
│       │   ├── ResumeAnalyzer.jsx  # AI resume features
│       │   ├── SavedJobs.jsx
│       │   ├── Login.jsx
│       │   └── About.jsx
│       ├── components/
│       │   ├── Navbar.jsx
│       │   ├── Footer.jsx
│       │   ├── JobCard.jsx
│       │   ├── AnimatedRadar.jsx   # Signature SVG visual
│       │   ├── AnimatedCounter.jsx
│       │   ├── AIChatWidget.jsx    # Floating AI chat
│       │   ├── SearchAutocomplete.jsx
│       │   ├── PageTransition.jsx
│       │   └── Skeleton.jsx
│       ├── context/
│       │   ├── ThemeContext.jsx
│       │   └── AuthContext.jsx
│       └── lib/api.js
│
└── docs/                         # Documentation
```

---

## Quick Setup (Local Development)

### Prerequisites

- **Python 3.10+** ([download](https://www.python.org/downloads/))
- **Node.js 18+** ([download](https://nodejs.org/))
- A **Supabase** account ([signup](https://supabase.com)) — free tier is enough
- Free API keys from the four job sources + Groq (see below)

### Step 1: Get Your API Keys (10 minutes)

All free, no credit card needed:

| Service | Sign up at | Free tier |
|---|---|---|
| Adzuna | https://developer.adzuna.com | 250 calls/month |
| RapidAPI (for JSearch) | https://rapidapi.com/letscrape-6bRBa3QguO5/api/jsearch | 200 calls/month |
| Jooble | https://jooble.org/api/about | Generous, host-restricted |
| Groq (AI features) | https://console.groq.com | 14,400 calls/day |
| Supabase | https://supabase.com | 500MB DB, free forever |

Remotive doesn't require a key.

### Step 2: Set Up the Database

1. In your Supabase dashboard → SQL Editor → New Query
2. Open `backend/data/schema.sql`, copy everything, paste in
3. Click **Run** → "Success, no rows returned"
4. Verify under Table Editor: you should see 7 tables (`jobs`, `skill_trends`, `role_clusters`, `skill_forecasts`, `app_users`, `saved_jobs`, `user_skills`)

### Step 3: Configure Backend

```bash
cd backend

# Create virtual environment
python -m venv venv

# Activate it (Windows)
venv\Scripts\activate
# Or Mac/Linux:
source venv/bin/activate

# Install dependencies (~2-3 min)
pip install -r requirements.txt
```

Copy `.env.example` to `.env`:

```bash
# Windows
copy .env.example .env
# Mac/Linux
cp .env.example .env
```

Open `.env` and fill in your API keys.

**Important:** The Supabase password must have `@` URL-encoded as `%40`. Use the **pooler URL** for Indian ISPs:

```
DATABASE_URL=postgresql://postgres.YOUR_REF:YOUR_PASSWORD@aws-1-ap-south-1.pooler.supabase.com:5432/postgres
```

### Step 4: Run the Backend

```bash
python app.py
```

You should see:

```
Starting SkillRadar API on port 5000
  Adzuna: configured
  Remotive: configured
  JSearch: configured
  Jooble: configured
  Database: connected
  Groq AI: connected
```

Test: open <http://localhost:5000/api/health> → JSON response.

### Step 5: Populate the Database

In a **new terminal**:

```bash
curl -X POST http://localhost:5000/api/jobs/ingest ^
  -H "Content-Type: application/json" ^
  -d "{\"queries\": [\"python developer\", \"data scientist\", \"react developer\", \"java developer\", \"devops engineer\"], \"location\": \"India\"}"
```

(Use `^` for Windows CMD, `\` for Mac/Linux.) Takes ~30 seconds.

### Step 6: Run the Frontend

In **another terminal**:

```bash
cd frontend
npm install
npm run dev
```

Open <http://localhost:5173>. SkillRadar is running!

---

## API Endpoints

22 REST endpoints total. Key ones:

### Jobs
- `GET /api/jobs/search?q=python&location=Pune` — Smart hybrid search
- `GET /api/jobs/saved-data` — Browse cached jobs
- `POST /api/jobs/ingest` — Fetch fresh + run NLP

### Skills
- `GET /api/skills/top` — Most demanded
- `GET /api/skills/trending` — Rising demand
- `GET /api/skills/emerging` — New in market
- `GET /api/skills/declining` — Losing demand
- `GET /api/skills/categories` — Grouped by category

### Analytics
- `GET /api/clusters` — K-Means role clusters
- `POST /api/clusters/refresh` — Recompute clusters
- `GET /api/forecast/<skill>` — 90-day demand forecast

### AI Features
- `POST /api/ai/resume/analyze` — Upload PDF, get full analysis
- `POST /api/ai/resume/tailor` — Generate tailoring suggestions
- `POST /api/ai/chat` — RAG-powered chat

### Other
- `GET /api/suggest?q=python` — Autocomplete
- `GET /api/health` — Health check
- User accounts + saved jobs

---

## Architecture

```
   ┌──────────────────────────────────────────────────────────┐
   │                      User Browser                        │
   │              React Frontend (Vercel)                     │
   └──────────────────────────┬───────────────────────────────┘
                              │
                              │  REST / JSON
                              ▼
   ┌──────────────────────────────────────────────────────────┐
   │              Flask Backend (Render / Local)              │
   ├──────────────────────────────────────────────────────────┤
   │                                                          │
   │  Aggregator → NLP Extractor → Trend Analyzer             │
   │      │            │                  │                   │
   │      ▼            ▼                  ▼                   │
   │   K-Means       Prophet         Groq LLM                 │
   │  Clustering   Forecasting       (RAG chat)               │
   │                                                          │
   └─┬────────────────┬────────────────┬─────────────────────┘
     │                │                │
     ▼                ▼                ▼
  ┌──────────┐  ┌───────────┐  ┌─────────────────┐
  │ Job APIs │  │ PostgreSQL│  │   Groq Cloud    │
  │ (4)      │  │ (Supabase)│  │  Llama 3.1 70B  │
  └──────────┘  └───────────┘  └─────────────────┘
```

---

## Production Deployment

### Backend → Render

1. Push code to GitHub
2. Go to [render.com](https://render.com) → New Web Service
3. Connect repo, settings:
   - **Root Directory:** `backend`
   - **Build:** `pip install -r requirements.txt`
   - **Start:** `gunicorn -w 2 -b 0.0.0.0:$PORT app:app`
4. Add environment variables (all keys from your `.env`)
5. Deploy → e.g. `https://skillradar-api.onrender.com`

### Frontend → Vercel

1. [vercel.com](https://vercel.com) → Import Project → select your repo
2. Settings:
   - **Root Directory:** `frontend`
   - **Framework:** Vite (auto-detected)
3. Add env var: `VITE_API_URL=https://skillradar-api.onrender.com`
4. Deploy → e.g. `https://skillradar.vercel.app`

**Note:** Render's free tier sleeps after 15 minutes of inactivity. First request after sleep takes ~30 seconds to wake up. Use [cron-job.org](https://cron-job.org) to ping it every 14 minutes if you need it always-on.

---

## Common Issues

| Problem | Fix |
|---|---|
| Backend says "Database: NOT connected" | Use Supabase pooler URL (not direct), URL-encode `@` as `%40` |
| Adzuna 403 Forbidden | Wrong app_id/key or hit 250/month limit |
| JSearch 429 Too Many Requests | Hit 200/month RapidAPI limit |
| Jooble 403 Host not in allowlist | Whitelist localhost in Jooble dashboard |
| Frontend blank page | Open browser console (F12) — usually a duplicate import |
| Prophet ModuleNotFoundError | OK — uses linear regression fallback automatically |
| PDF upload fails | Run `pip install pypdf` |
| Search slow first time | DB-first search, but live API top-up takes 5-10s on cold cache |

---

## Performance Notes

- **Parallel API calls** via `ThreadPoolExecutor` — 4 APIs in ~5 seconds vs 20 sequentially
- **Cache-first search** — DB returns in <1s, only hits live APIs if needed
- **Deduplication** by `(title + company + location)` signature
- **Auto-augmented forecasting** — fills sparse time-series with weekly seasonality baseline
- **Hot-reload** in dev — frontend updates instantly, backend on file save

---

## Security

- All secrets in `.env` (never committed)
- `.env.example` shows required vars without real values
- SQL injection prevented via parameterized queries
- CORS restricted in production
- Rate limiting via cache TTL on external APIs

---

## License

This is an academic project. Code shared for educational reference.

---

## Contributing

This is a final-year academic project — not open for external contributions. Feel free to fork for your own learning.
