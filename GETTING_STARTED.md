# Getting Started With SkillRadar

This guide walks you through running SkillRadar locally in about **15 minutes**.

## What You're Building

A complete real-time job market intelligence platform with:

- ✅ Live data from 4 sources: Adzuna, Remotive, JSearch (LinkedIn/Indeed/Glassdoor), Jooble
- ✅ NLP skill extraction (214 skills taxonomy, 17 categories)
- ✅ Trend analysis (top, trending, emerging, declining)
- ✅ K-Means role clustering
- ✅ Time-series demand forecasting (Prophet + linear fallback)
- ✅ **AI Resume Analyzer** with PDF upload, job matching, skill gaps, learning resources
- ✅ **AI Chat Widget** powered by Groq Llama 3.1 70B with RAG
- ✅ Premium React frontend with animated radar, light/dark themes
- ✅ User accounts and saved jobs

---

## What You Need to Install

1. **Python 3.10 or higher** — https://www.python.org/downloads/
   - **Important:** Check "Add Python to PATH" during install
2. **Node.js 18 or higher** — https://nodejs.org/
3. **VS Code** (recommended) — https://code.visualstudio.com/

---

## Step 1: Open the Project

Extract the project zip. Open the `skillradar` folder in VS Code.

---

## Step 2: Set Up Supabase Database (5 minutes)

1. Sign up at https://supabase.com (free)
2. Create a new project — note the password you set
3. Once provisioned, go to **SQL Editor** in the sidebar
4. Click **New Query**
5. Open `backend/data/schema.sql` from your project folder
6. Copy **all** the contents, paste into the SQL editor
7. Click **Run** (or Ctrl+Enter)
8. Should see "Success, no rows returned"
9. Click **Table Editor** in sidebar — you should see 7 new tables

---

## Step 3: Get Your API Keys (10 minutes)

All free. No credit card required.

### 3a. Adzuna (Indian job market)

1. https://developer.adzuna.com → Sign up
2. After login → "Create Application"
3. Copy `Application ID` and `Application Key`

### 3b. RapidAPI (for JSearch — LinkedIn/Indeed/Glassdoor)

1. https://rapidapi.com → Sign up with Google
2. Search for "JSearch" → subscribe to the **free Basic plan**
3. Click "Endpoints" → copy `X-RapidAPI-Key` value

### 3c. Jooble (extra job source)

1. https://jooble.org/api/about → Apply for API access
2. Wait for approval email (usually instant)
3. Copy your API key

### 3d. Groq (AI features)

1. https://console.groq.com → Sign in with Google
2. API Keys → Create API Key → name it `skillradar`
3. Copy the key (starts with `gsk_`)

### 3e. Supabase

1. In your Supabase project → Settings → Database
2. Copy the **connection string** under "Connection pooling" (not direct)
3. Should look like:
   ```
   postgresql://postgres.YOUR_REF:[PASSWORD]@aws-1-ap-south-1.pooler.supabase.com:5432/postgres
   ```
4. Replace `[PASSWORD]` with your actual password
5. **Important:** If your password has `@` in it, change to `%40`

---

## Step 4: Configure Backend (.env file)

1. In VS Code, navigate to `backend/`
2. Copy `.env.example` to `.env` (right-click → Copy → Paste)
3. Open `.env` and fill in your keys:

```env
FLASK_ENV=development
FLASK_PORT=5000
SECRET_KEY=any-random-string-here

DATABASE_URL=postgresql://postgres.xxxxx:YourPass%40123@aws-1-ap-south-1.pooler.supabase.com:5432/postgres
SUPABASE_URL=https://your-ref.supabase.co
SUPABASE_ANON_KEY=your_anon_key_from_supabase_dashboard

ADZUNA_APP_ID=your_app_id
ADZUNA_APP_KEY=your_app_key

RAPIDAPI_KEY=your_rapidapi_key

JOOBLE_API_KEY=your_jooble_key

GROQ_API_KEY=your_groq_key

CACHE_DIR=./cache
CACHE_TTL_HOURS=6
```

Save the file.

⚠️ **Never commit this file to GitHub.** It's already in `.gitignore`.

---

## Step 5: Run the Backend

Open a terminal in VS Code (Terminal → New Terminal).

```bash
cd backend

# Create virtual environment
python -m venv venv

# Activate it (Windows)
venv\Scripts\activate

# Or Mac/Linux
source venv/bin/activate

# Install all packages (~2-3 minutes)
pip install -r requirements.txt
```

If `prophet` fails, that's OK — the forecaster has a built-in linear regression fallback.

Now start the backend:

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

✅ Backend is running. Keep this terminal open.

**Quick test:** Open <http://localhost:5000/api/health> in your browser. You should see JSON.

---

## Step 6: Populate the Database (2 minutes)

Open a **new terminal** (keep the first one running).

Windows CMD/PowerShell:

```cmd
curl -X POST http://localhost:5000/api/jobs/ingest -H "Content-Type: application/json" -d "{\"queries\": [\"python developer\", \"data scientist\", \"react developer\", \"java developer\", \"devops engineer\"], \"location\": \"India\"}"
```

Mac/Linux:

```bash
curl -X POST http://localhost:5000/api/jobs/ingest \
  -H "Content-Type: application/json" \
  -d '{"queries": ["python developer", "data scientist", "react developer", "java developer", "devops engineer"], "location": "India"}'
```

Takes about 30 seconds. You'll see a response showing how many jobs were saved.

---

## Step 7: Run the Frontend

In the same second terminal:

```bash
cd ../frontend

# Install packages (~2-3 min)
npm install

# Start the frontend
npm run dev
```

You'll see:

```
  VITE v5.x ready in 800 ms
  ➜  Local:   http://localhost:5173/
```

✅ Open <http://localhost:5173> — SkillRadar is now running!

---

## Things to Try

### Core Features
1. **Home page** — See the animated radar visualization
2. **Jobs page** — Search "python developer in Pune"
3. **Skills page** — Browse top skills, trending, emerging, categories
4. **Roles page** — Click "Refresh Clusters" to run K-Means live
5. **Forecast page** — See demand predictions for top skills

### AI Features
6. **Resume AI** — Upload your resume PDF
   - See extracted skills, target roles
   - View matching jobs with match scores
   - Check skill gaps with learning resources
   - Click "AI Tailor" on any job for personalized suggestions
7. **AI Chat** — Click the floating chat button (bottom-right)
   - Ask: "What's trending in tech?"
   - Ask: "Should I learn Rust or Go?"
   - Real LLM responses grounded in your real data (RAG)

### Other
8. **Sign in** — Use any email (no password required for demo)
9. **Save jobs** — Bookmark icon on any job card
10. **Theme toggle** — Top-right corner, switch light/dark

---

## When You're Done Testing

Press `Ctrl+C` in both terminals to stop everything.

---

## Common Issues

| Problem | Fix |
|---|---|
| `python is not recognized` | Reinstall Python with "Add to PATH" checked |
| `npm is not recognized` | Reinstall Node.js, restart terminal |
| Backend says `Database: NOT connected` | Use **pooler** URL, encode `@` as `%40` |
| `Adzuna: MISSING` on startup | Check your `.env` keys are correct |
| `Jooble: 403 Host not in allowlist` | Whitelist `localhost` in Jooble dashboard |
| Frontend shows "Could not fetch jobs" | Backend not running — check first terminal |
| Frontend blank page | Open F12 → Console → check for errors |
| PDF upload says "pypdf not found" | Run `pip install pypdf` in backend venv |
| Search returns only 6 jobs | DB needs more data — re-run Step 6 with more queries |

---

## Next Steps

1. Read `README.md` for full project documentation
2. Read `backend/SETUP.md` for API endpoint details
3. Read `docs/PROJECT_REPORT_CONTENT.md` for project report content
4. Push to GitHub when ready (`.env` is already in `.gitignore`)
5. Deploy to Vercel + Render (deployment instructions in `README.md`)

---

## Project Customization Tips

- **Add more job queries**: Modify the Step 6 curl command with your own keywords
- **Adjust forecast horizon**: Change days param in `/api/forecast/<skill>?days=N`
- **Change AI model**: Edit `backend/ai/groq_client.py` — try `llama-3.1-8b-instant` for faster (less accurate)
- **Change theme colors**: Edit `frontend/tailwind.config.js` `brand` palette
- **Add a new job source**: Use existing clients as template (`backend/services/`)
