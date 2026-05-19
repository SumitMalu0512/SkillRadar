# Deployment Guide

This guide deploys SkillRadar to production using free tiers:
- **Backend** → Render (Flask API)
- **Frontend** → Vercel (React app)
- **Database** → Supabase (already deployed during setup)

Total cost: **$0/month**.

---

## Pre-Deployment Checklist

Before deploying, make sure:

- [ ] You have a working local setup (tested with `npm run dev` and `python app.py`)
- [ ] Your code is pushed to GitHub
- [ ] `.env` is **NOT** committed (verify in your GitHub repo — should be missing)
- [ ] `.env.example` **IS** committed with placeholder values
- [ ] `requirements.txt` exists in `backend/`
- [ ] `package.json` exists in `frontend/`

### Rotate Your Keys Before Pushing!

If you've been sharing this project (chat, email, etc.) and your `.env` was visible anywhere, **regenerate every key before going public**:

1. Adzuna → revoke old, create new
2. RapidAPI → reset key
3. Jooble → request new key
4. Groq → revoke old, create new
5. Supabase → reset database password
6. Update your local `.env` with new keys

This is critical — leaked keys can be abused by bots scanning GitHub.

---

## Step 1: Push to GitHub

```bash
# In your project root
cd D:\FiY Project\skillradar

# Initialize git (if not already)
git init

# Verify .env is gitignored
git status
# You should NOT see backend/.env in the output

# Stage everything
git add .

# Commit
git commit -m "Initial deployment commit"

# Create a new repo on github.com (private or public)
# Then connect and push:
git remote add origin https://github.com/YOUR_USERNAME/skillradar.git
git branch -M main
git push -u origin main
```

---

## Step 2: Deploy Backend to Render

### 2a. Create Render Account
1. Sign up at https://render.com (use GitHub for fastest signup)
2. Free tier — no credit card needed

### 2b. Create Web Service
1. Dashboard → **New +** → **Web Service**
2. Connect your GitHub account
3. Select the `skillradar` repository
4. Configure:

| Field | Value |
|---|---|
| **Name** | `skillradar-api` |
| **Region** | Singapore (closest to India) |
| **Branch** | `main` |
| **Root Directory** | `backend` |
| **Runtime** | Python 3 |
| **Build Command** | `pip install -r requirements.txt` |
| **Start Command** | `gunicorn -w 2 -b 0.0.0.0:$PORT app:app` |
| **Plan** | Free |

### 2c. Add Environment Variables

Click **Advanced** → **Add Environment Variable** and add each key from your `.env`:

```
FLASK_ENV=production
FLASK_PORT=10000          (Render uses this)
SECRET_KEY=<your secret>
DATABASE_URL=<your supabase pooler url>
SUPABASE_URL=<your supabase url>
SUPABASE_ANON_KEY=<your anon key>
ADZUNA_APP_ID=<your id>
ADZUNA_APP_KEY=<your key>
RAPIDAPI_KEY=<your key>
JOOBLE_API_KEY=<your key>
GROQ_API_KEY=<your key>
CACHE_DIR=./cache
CACHE_TTL_HOURS=12
```

### 2d. Deploy

Click **Create Web Service**. Render will:
1. Clone your repo
2. Install Python dependencies (~3 min)
3. Start the server

You'll get a URL like: `https://skillradar-api.onrender.com`

**Test it:** Open `https://skillradar-api.onrender.com/api/health` — should return JSON.

### 2e. Whitelist for External APIs (if needed)

If Jooble or Adzuna restrict by host, add your Render URL to their allowlists.

---

## Step 3: Deploy Frontend to Vercel

### 3a. Update Frontend Config

In your local `frontend/` folder, create a `.env.production` file:

```env
VITE_API_URL=https://skillradar-api.onrender.com
```

Commit and push:

```bash
git add frontend/.env.production
git commit -m "Add production API URL"
git push
```

### 3b. Deploy on Vercel

1. Sign up at https://vercel.com (use GitHub)
2. Dashboard → **Add New** → **Project**
3. Import your `skillradar` GitHub repo
4. Configure:

| Field | Value |
|---|---|
| **Framework Preset** | Vite (auto-detected) |
| **Root Directory** | `frontend` |
| **Build Command** | `npm run build` (default) |
| **Output Directory** | `dist` (default) |
| **Install Command** | `npm install` (default) |

### 3c. Environment Variables (Vercel)

Add this in the Vercel project settings:

```
VITE_API_URL=https://skillradar-api.onrender.com
```

### 3d. Deploy

Click **Deploy**. Vercel will:
1. Clone the repo
2. Install npm packages (~2 min)
3. Build the React app
4. Deploy to CDN

You'll get a URL like: `https://skillradar.vercel.app`

---

## Step 4: Configure CORS (Backend ↔ Frontend)

The backend needs to allow your Vercel domain. Check `backend/app.py` for CORS config:

```python
from flask_cors import CORS
CORS(app, origins=["https://skillradar.vercel.app", "http://localhost:5173"])
```

If you need to update this, push the change to GitHub — Render auto-redeploys.

---

## Step 5: Keep Backend Awake (Optional)

Render free tier **sleeps after 15 minutes of inactivity**. First request after sleep takes ~30 seconds (the "cold start").

To keep it awake:

1. Sign up at https://cron-job.org (free)
2. Create a new cron job:
   - **URL:** `https://skillradar-api.onrender.com/api/health`
   - **Schedule:** Every 14 minutes
   - **Method:** GET
3. Save

Your backend stays warm 24/7 for free.

---

## Step 6: Final Verification

1. Open `https://skillradar.vercel.app` in incognito mode
2. Search for "python developer" → results appear
3. Click "Resume AI" → upload a PDF → matches appear
4. Click the floating chat button → ask a question → real LLM response
5. Toggle dark/light mode → smooth transition
6. Mobile test: open on phone or browser DevTools mobile mode

If anything fails, check:
- Browser console (F12) for frontend errors
- Render dashboard → Logs for backend errors
- Supabase dashboard → Logs for database queries

---

## Custom Domain (Optional)

### Vercel
1. Buy a domain (Namecheap, GoDaddy, or use a free `.tk`)
2. Vercel → Project Settings → Domains → Add
3. Update DNS records per Vercel's instructions

### Render
Same flow on Render → Settings → Custom Domains.

---

## Costs Summary

| Service | Plan | Limits | Cost |
|---|---|---|---|
| Vercel | Hobby | 100GB bandwidth, unlimited deployments | $0 |
| Render | Free | 750 hours/month, sleeps after 15min | $0 |
| Supabase | Free | 500MB DB, 50K monthly users | $0 |
| GitHub | Free | Unlimited public repos | $0 |
| **Total** | | | **$0/month** |

API calls are limited by the providers:
- Adzuna: 250/month free
- RapidAPI JSearch: 200/month free
- Groq: 14,400/day free (plenty)
- Jooble: free with host restriction
- Remotive: no limit

---

## Troubleshooting

| Symptom | Likely Cause | Fix |
|---|---|---|
| Render build fails on `prophet` install | Prophet needs more memory than free tier | Use linear fallback (already built-in). Remove `prophet` from requirements.txt |
| Frontend shows CORS error | Backend doesn't allow Vercel domain | Add domain to CORS list in `app.py` |
| Backend says "Database: NOT connected" | DATABASE_URL not set in Render env vars | Re-add in Render dashboard |
| "Application Error" page on Render | Crash on startup | Check Render logs for traceback |
| Search returns 0 results | Database empty | Re-run the `/api/jobs/ingest` curl command pointed at production URL |
| AI chat doesn't work | GROQ_API_KEY missing | Add in Render env vars |
| Vercel build fails | Missing env var | Add `VITE_API_URL` in Vercel settings |

---

## Post-Deployment Steps

1. ⭐ Star your own GitHub repo (looks better on profile)
2. Add the live demo URL to your repo README
3. Take screenshots of the deployed app for your project report
4. If demoing in viva: have a backup screenshot in case Render is sleeping
5. **Rotate keys** if you've shared them anywhere

You're live! 🚀
