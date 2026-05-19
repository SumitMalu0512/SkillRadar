"""
SkillRadar Flask API

Main entry point - exposes all endpoints the frontend uses:
  GET  /api/health               - health check
  GET  /api/jobs/search          - search live jobs from APIs
  POST /api/jobs/ingest          - fetch + extract + save to DB (background job)
  GET  /api/jobs/saved           - get saved/cached jobs from DB
  GET  /api/skills/top           - top skills overall
  GET  /api/skills/trending      - trending skills (with growth)
  GET  /api/skills/emerging      - emerging skills
  GET  /api/skills/declining     - declining skills
  GET  /api/skills/categories    - skill category distribution
  POST /api/skills/extract       - extract skills from a text (for resume analyzer)
  GET  /api/clusters             - get all job role clusters
  POST /api/clusters/refresh     - re-run clustering on current data
  GET  /api/forecast/<skill>     - get forecast for a single skill
  POST /api/users/register       - create/login a user (email-based)
  GET  /api/users/<id>/saved     - get user's saved jobs
  POST /api/users/<id>/save      - save a job
  DELETE /api/users/<id>/save/<job_id> - unsave a job
"""
import os
from datetime import datetime
from flask import Flask, request, jsonify
from flask_cors import CORS
from dotenv import load_dotenv

# load env first thing
load_dotenv()

from config import config
from services import AdzunaClient, RemotiveClient, JSearchClient, JoobleClient, JobAggregator
from nlp import get_extractor
from nlp.trend_analyzer import get_analyzer
from ml import RoleClusterer, SkillForecaster
from ai import ResumeParser, JobMatcher, GroqClient, ContextBuilder, resources_for_skill
from utils import FileCache
from data import Database


# ---------------- App setup ----------------

app = Flask(__name__)
CORS(app, resources={r"/api/*": {"origins": "*"}})

# Build shared service instances ONCE at startup (instead of per-request)
cache = FileCache(cache_dir=config.CACHE_DIR, ttl_hours=config.CACHE_TTL_HOURS)

adzuna = AdzunaClient(config.ADZUNA_APP_ID, config.ADZUNA_APP_KEY, cache=cache) \
    if config.ADZUNA_APP_ID else None
remotive = RemotiveClient(cache=cache)
jsearch = JSearchClient(config.RAPIDAPI_KEY, cache=cache) \
    if config.RAPIDAPI_KEY else None
jooble = JoobleClient(config.JOOBLE_API_KEY, cache=cache) \
    if config.JOOBLE_API_KEY else None

aggregator = JobAggregator(adzuna=adzuna, remotive=remotive, jsearch=jsearch, jooble=jooble)
extractor = get_extractor()
analyzer = get_analyzer()
forecaster = SkillForecaster()

# AI services
resume_parser = ResumeParser(skill_extractor=extractor)
job_matcher = JobMatcher()
groq = GroqClient(api_key=os.getenv("GROQ_API_KEY", ""))
if groq.is_available:
    print("[AI] Groq LLM connected")
else:
    print("[AI] Groq API key not set - chat will use fallback responses")
context_builder = None    # will init after db is ready

# Database - only init if DATABASE_URL is real
db = None
if config.DATABASE_URL and not config.DATABASE_URL.startswith("sqlite"):
    try:
        db = Database(config.DATABASE_URL)
        # test the connection
        with db.cursor() as cur:
            cur.execute("SELECT 1")
        print("[DB] Connected to PostgreSQL successfully")
    except Exception as e:
        print(f"[DB] Could not connect: {e}")
        db = None

# Now we have db, set up context builder
context_builder = ContextBuilder(db=db, analyzer=analyzer)

# Global cached clusterer (refreshed on demand)
_clusterer = None


# ---------------- ROUTES ----------------

@app.route("/api/health")
def health():
    return jsonify({
        "status": "ok",
        "service": "SkillRadar API",
        "version": "1.0.0",
        "time": datetime.now().isoformat(),
        "components": {
            "adzuna": adzuna is not None,
            "remotive": remotive is not None,
            "jsearch": jsearch is not None,
            "database": db is not None,
        },
    })


@app.route("/api/jobs/search")
def search_jobs():
    """
    Smart job search:
      - Returns DB results immediately (fast)
      - If DB has fewer than the requested limit, supplements with live API results
      - If live=true is passed, skips cache and always hits APIs
      - New live results auto-saved to DB so next search is faster

    Query params: q, location, remote, limit, live
    """
    q = request.args.get("q", "").strip()
    location = request.args.get("location", "India").strip()
    remote = request.args.get("remote", "").lower() in ("true", "1", "yes")
    limit = min(int(request.args.get("limit", 200)), 500)
    force_live = request.args.get("live", "").lower() in ("true", "1", "yes")

    # Threshold: if DB has at least this many results, skip live API call
    MIN_RESULTS = max(30, limit // 3)

    job_dicts = []
    source = "db"

    # Step 1: try DB first (fast)
    if db and not force_live:
        try:
            is_remote = True if remote else None
            db_jobs = db.search_jobs(
                query=q if q else None,
                location=location if location and location.lower() != "worldwide" else None,
                is_remote=is_remote,
                limit=limit,
                offset=0,
            )
            if db_jobs:
                job_dicts = db_jobs
        except Exception as e:
            print(f"[search] DB query failed, falling back to live: {e}")

    # Step 2: if DB returned too few, supplement with live API
    if force_live or len(job_dicts) < MIN_RESULTS:
        source = "live" if not job_dicts else "hybrid"
        try:
            jobs = aggregator.search(query=q, location=location, remote_only=remote, limit=limit)
            for job in jobs:
                if not job.extracted_skills:
                    job.extracted_skills = extractor.extract(job.description or "")
            live_dicts = [j.to_dict() for j in jobs]

            # save to DB so next search is fast
            if db and live_dicts:
                try:
                    db.bulk_upsert_jobs(live_dicts)
                except Exception as e:
                    print(f"[DB] Background save failed: {e}")

            # merge with DB results - dedupe by job_id
            seen_ids = {j.get("job_id") for j in job_dicts}
            for j in live_dicts:
                if j.get("job_id") not in seen_ids:
                    job_dicts.append(j)
                    seen_ids.add(j.get("job_id"))
        except Exception as e:
            print(f"[search] Live API call failed: {e}")

    # cap to limit
    job_dicts = job_dicts[:limit]

    # Build stats
    stats = {
        "total": len(job_dicts),
        "remote_count": sum(1 for j in job_dicts if j.get("is_remote")),
        "by_source": {},
    }
    for j in job_dicts:
        src = j.get("source", "unknown")
        stats["by_source"][src] = stats["by_source"].get(src, 0) + 1

    return jsonify({
        "query": q,
        "location": location,
        "source": source,
        "stats": stats,
        "results": job_dicts,
    })


@app.route("/api/jobs/saved-data")
def saved_jobs_from_db():
    """Browse pre-ingested jobs from the database. Faster than live search."""
    if not db:
        return jsonify({"error": "Database not configured"}), 503

    q = request.args.get("q")
    location = request.args.get("location")
    skill = request.args.get("skill")
    remote = request.args.get("remote")
    is_remote = None
    if remote:
        is_remote = remote.lower() in ("true", "1", "yes")
    limit = min(int(request.args.get("limit", 50)), 200)
    offset = int(request.args.get("offset", 0))

    jobs = db.search_jobs(
        query=q, location=location, skill=skill,
        is_remote=is_remote, limit=limit, offset=offset,
    )
    return jsonify({
        "total": db.count_jobs(),
        "returned": len(jobs),
        "results": jobs,
    })


@app.route("/api/jobs/ingest", methods=["POST"])
def ingest_jobs():
    """
    Trigger a fresh fetch + extract + save cycle.
    Useful to populate the DB for analytics.
    """
    data = request.json or {}
    queries = data.get("queries", ["software developer", "data scientist", "python developer"])
    location = data.get("location", "India")

    all_jobs = []
    for q in queries:
        jobs = aggregator.search(query=q, location=location, limit=30)
        for j in jobs:
            if not j.extracted_skills:
                j.extracted_skills = extractor.extract(j.description or "")
        all_jobs.extend(jobs)

    job_dicts = [j.to_dict() for j in all_jobs]

    saved = 0
    if db:
        try:
            db.bulk_upsert_jobs(job_dicts)
            saved = len(job_dicts)
        except Exception as e:
            return jsonify({"error": str(e)}), 500

    return jsonify({
        "fetched": len(job_dicts),
        "saved": saved,
        "queries": queries,
    })


@app.route("/api/skills/top")
def top_skills():
    limit = int(request.args.get("limit", 20))
    jobs = _get_jobs_for_analysis()
    return jsonify({"results": analyzer.top_skills(jobs, top_n=limit)})


@app.route("/api/skills/trending")
def trending_skills():
    limit = int(request.args.get("limit", 15))
    jobs = _get_jobs_for_analysis()
    return jsonify({"results": analyzer.trending_skills(jobs, top_n=limit)})


@app.route("/api/skills/emerging")
def emerging_skills():
    limit = int(request.args.get("limit", 10))
    jobs = _get_jobs_for_analysis()
    return jsonify({"results": analyzer.emerging_skills(jobs, top_n=limit)})


@app.route("/api/skills/declining")
def declining_skills():
    limit = int(request.args.get("limit", 10))
    jobs = _get_jobs_for_analysis()
    return jsonify({"results": analyzer.declining_skills(jobs, top_n=limit)})


@app.route("/api/skills/categories")
def skill_categories():
    jobs = _get_jobs_for_analysis()
    return jsonify({"distribution": analyzer.category_distribution(jobs)})


@app.route("/api/skills/extract", methods=["POST"])
def extract_skills():
    """For users to paste their resume / a JD and extract skills."""
    data = request.json or {}
    text = data.get("text", "")
    if not text:
        return jsonify({"error": "Missing 'text' field"}), 400
    details = extractor.extract_with_details(text)
    return jsonify({"skills": details, "total": len(details)})


@app.route("/api/suggest")
def suggest():
    """
    Autocomplete suggestions for the search box.
    Combines: real job titles from DB + skills taxonomy + curated role list + companies.
    Ordered so the most useful suggestions appear first.
    """
    q = request.args.get("q", "").strip().lower()
    limit = int(request.args.get("limit", 8))

    if not q or len(q) < 1:
        return jsonify({"suggestions": []})

    suggestions = []
    seen = set()

    def add(value, type_, category=""):
        """Add a suggestion if not already present."""
        key = value.lower().strip()
        if key and key not in seen and len(suggestions) < limit:
            seen.add(key)
            suggestions.append({"value": value, "type": type_, "category": category})

    # 1. Real job titles from the database (the most useful suggestions)
    if db:
        try:
            with db.cursor() as cur:
                # find distinct job titles matching the query, ordered by frequency
                cur.execute(
                    """
                    SELECT title, COUNT(*) as cnt
                    FROM jobs
                    WHERE LOWER(title) LIKE %s
                    GROUP BY title
                    ORDER BY cnt DESC, title
                    LIMIT 6
                    """,
                    (f"%{q}%",),
                )
                for row in cur.fetchall():
                    add(row["title"], "role", f"{row['cnt']} jobs")
        except Exception as e:
            print(f"[suggest] DB title query failed: {e}")

    # 2. Skill taxonomy matches
    from nlp.skill_taxonomy import SKILL_TAXONOMY
    skill_matches = []
    for skill_name, info in SKILL_TAXONOMY.items():
        sl = skill_name.lower()
        if q in sl:
            skill_matches.append((sl.index(q), len(skill_name), skill_name, info.get("category", "")))
        else:
            for alias in info.get("aliases", []):
                if q in alias.lower():
                    skill_matches.append((99, len(skill_name), skill_name, info.get("category", "")))
                    break
    skill_matches.sort()
    for _, _, name, cat in skill_matches:
        add(name, "skill", cat)

    # 3. Common role suggestions - exhaustive list covering most tech & non-tech roles
    common_roles = [
        # Software / Engineering
        "Software Engineer", "Software Developer", "Senior Software Engineer",
        "Software Engineer Intern", "Junior Software Engineer", "Software Architect",
        "Principal Software Engineer", "Staff Software Engineer", "Lead Software Engineer",
        "SDE", "SDE 1", "SDE 2", "SDE 3",
        # Web / Stack
        "Frontend Developer", "Backend Developer", "Full Stack Developer", "Full Stack Engineer",
        "Senior Frontend Developer", "Senior Backend Developer", "Web Developer",
        "Web Designer", "UI Developer",
        # Specific stack
        "Python Developer", "Java Developer", "C++ Developer", "C# Developer",
        "Node.js Developer", "React Developer", "Angular Developer", "Vue.js Developer",
        ".NET Developer", "Golang Developer", "Ruby on Rails Developer", "PHP Developer",
        "Java Backend Developer", "Python Backend Developer", "TypeScript Developer",
        # Mobile
        "Mobile Developer", "Android Developer", "iOS Developer", "React Native Developer",
        "Flutter Developer", "Mobile App Developer",
        # Data
        "Data Scientist", "Senior Data Scientist", "Data Analyst", "Data Engineer",
        "Senior Data Engineer", "Analytics Engineer", "Business Intelligence Developer",
        "BI Developer", "ETL Developer", "Big Data Engineer",
        # AI / ML
        "Machine Learning Engineer", "ML Engineer", "AI Engineer", "Deep Learning Engineer",
        "MLOps Engineer", "AI Research Scientist", "NLP Engineer", "Computer Vision Engineer",
        "Generative AI Engineer", "LLM Engineer",
        # Cloud / DevOps
        "DevOps Engineer", "Cloud Engineer", "Site Reliability Engineer", "SRE",
        "Cloud Architect", "AWS Engineer", "Azure Engineer", "GCP Engineer",
        "Platform Engineer", "Infrastructure Engineer", "Build Engineer",
        # QA / Testing
        "QA Engineer", "QA Analyst", "Test Engineer", "Test Automation Engineer",
        "Manual Tester", "Performance Test Engineer", "SDET",
        # Security
        "Security Engineer", "Cybersecurity Analyst", "Penetration Tester",
        "Information Security Analyst", "Security Architect", "SOC Analyst",
        # Database
        "Database Administrator", "DBA", "Database Engineer", "Database Developer",
        # Design
        "UI UX Designer", "UX Designer", "UI Designer", "Product Designer",
        "Visual Designer", "Graphic Designer", "Interaction Designer",
        # Product / Management
        "Product Manager", "PM", "Senior Product Manager", "Associate Product Manager", "APM",
        "Technical Product Manager", "TPM", "Product Owner", "PO", "Project Manager",
        "Program Manager", "Technical Program Manager", "Engineering Manager", "EM",
        "Technical Lead", "Tech Lead", "Team Lead", "TL", "Delivery Manager",
        # Business / Functional
        "Business Analyst", "BA", "Senior Business Analyst", "Functional Analyst",
        "Systems Analyst", "Business Intelligence Analyst", "Reporting Analyst",
        # Architecture
        "Solutions Architect", "Enterprise Architect", "Data Architect",
        "Technical Architect", "Cloud Solutions Architect",
        # Other tech
        "Salesforce Developer", "SAP Consultant", "ServiceNow Developer",
        "Embedded Software Engineer", "Firmware Engineer", "Game Developer",
        "Blockchain Developer", "Web3 Developer", "Robotics Engineer",
        # Support / Operations
        "Technical Support Engineer", "Customer Success Engineer", "DevOps Lead",
        "Release Engineer", "Operations Engineer",
        # Internships / Entry level
        "Software Developer Intern", "Data Science Intern", "Web Developer Intern",
        "Backend Developer Intern", "Frontend Developer Intern",
    ]

    # smarter matching: substring OR every query word matches start of some role word
    role_matches = []
    q_words = q.split()
    for r in common_roles:
        rl = r.lower()
        if q in rl:
            role_matches.append((rl.index(q), len(r), r))
        elif len(q_words) > 1 and all(any(word.startswith(qw) for word in rl.split()) for qw in q_words):
            role_matches.append((50, len(r), r))
    role_matches.sort()
    for _, _, r in role_matches:
        add(r, "role")

    # 4. Companies from the database
    if db and len(suggestions) < limit:
        try:
            with db.cursor() as cur:
                cur.execute(
                    """
                    SELECT DISTINCT company FROM jobs
                    WHERE LOWER(company) LIKE %s
                    LIMIT 4
                    """,
                    (f"%{q}%",),
                )
                for row in cur.fetchall():
                    name = row["company"]
                    if name:
                        add(name, "company")
        except Exception:
            pass

    return jsonify({"suggestions": suggestions[:limit]})


@app.route("/api/clusters")
def get_clusters():
    """Return current cluster summary."""
    if db:
        clusters = db.get_clusters()
        if clusters:
            # parse JSONB top_skills
            for c in clusters:
                import json as _json
                if isinstance(c.get("top_skills"), str):
                    try:
                        c["top_skills"] = _json.loads(c["top_skills"])
                    except Exception:
                        c["top_skills"] = []
                if "last_updated" in c and c["last_updated"]:
                    c["last_updated"] = c["last_updated"].isoformat() if hasattr(c["last_updated"], "isoformat") else str(c["last_updated"])
            return jsonify({"clusters": clusters})

    # fallback: cluster live
    global _clusterer
    if _clusterer is None:
        jobs = _get_jobs_for_analysis()
        if len(jobs) < 16:
            return jsonify({"clusters": [], "message": "Not enough data yet. Ingest more jobs first."})
        _clusterer = RoleClusterer(n_clusters=6)
        _clusterer.fit(jobs)
    return jsonify({"clusters": _clusterer.get_clusters_summary(jobs)})


@app.route("/api/clusters/refresh", methods=["POST"])
def refresh_clusters():
    """Re-run clustering on current data."""
    global _clusterer
    jobs = _get_jobs_for_analysis()
    if len(jobs) < 16:
        return jsonify({"error": "Need at least 16 jobs with skills to cluster"}), 400

    n_clusters = int(request.json.get("n_clusters", 6)) if request.json else 6
    _clusterer = RoleClusterer(n_clusters=n_clusters)
    result = _clusterer.fit(jobs)
    summary = _clusterer.get_clusters_summary(jobs)

    if db:
        try:
            db.save_clusters(summary)
        except Exception as e:
            print(f"[DB] Could not save clusters: {e}")

    return jsonify({"result": result, "summary": summary})


@app.route("/api/forecast/<skill>")
def forecast(skill: str):
    days = int(request.args.get("days", 90))
    jobs = _get_jobs_for_analysis()
    result = forecaster.forecast_skill(jobs, skill, forecast_days=days)
    if not result:
        return jsonify({"error": f"Not enough data to forecast '{skill}'"}), 404
    return jsonify(result)


@app.route("/api/forecast/top/all")
def forecast_top():
    top_n = int(request.args.get("top", 8))
    days = int(request.args.get("days", 90))
    jobs = _get_jobs_for_analysis()
    forecasts = forecaster.forecast_top_skills(jobs, top_n=top_n, forecast_days=days)
    return jsonify({"forecasts": forecasts})


# ---------------- AI FEATURES ----------------

@app.route("/api/ai/resume/analyze", methods=["POST"])
def analyze_resume():
    """
    Upload a PDF resume and get structured analysis with extracted skills,
    target roles, and matching jobs.
    Expects multipart/form-data with a 'file' field.
    """
    if "file" not in request.files:
        return jsonify({"error": "No file uploaded. Use multipart/form-data with 'file' field."}), 400

    f = request.files["file"]
    if not f.filename:
        return jsonify({"error": "Empty filename"}), 400

    if not f.filename.lower().endswith(".pdf"):
        return jsonify({"error": "Only PDF files are supported"}), 400

    pdf_bytes = f.read()
    if len(pdf_bytes) > 10 * 1024 * 1024:
        return jsonify({"error": "File too large (max 10 MB)"}), 400

    # parse the PDF
    parsed = resume_parser.parse_pdf(pdf_bytes)
    if parsed.get("error"):
        return jsonify(parsed), 400

    # find matching jobs from the database
    jobs_pool = _get_jobs_for_analysis()
    matched = job_matcher.score_jobs(parsed["skills"], jobs_pool)
    top_matches = matched[:20]

    # skill gaps and strengths against the market
    gaps = job_matcher.compute_skill_gaps(parsed["skills"], jobs_pool, top_n=12)
    # attach learning resources to each gap
    for g in gaps:
        g["learning_resources"] = resources_for_skill(g["skill"], limit=3)
    strengths = job_matcher.strengths(parsed["skills"], jobs_pool, top_n=8)

    return jsonify({
        "resume": {
            "name": parsed.get("name", ""),
            "email": parsed.get("email", ""),
            "experience_years": parsed.get("experience_years"),
            "experience_level": parsed.get("experience_level"),
            "target_roles": parsed.get("target_roles", []),
            "skills": parsed["skills"],
            "skill_details": parsed.get("skill_details", []),
            "word_count": parsed.get("word_count", 0),
        },
        "matched_jobs": top_matches,
        "skill_gaps": gaps,
        "strengths": strengths,
        "stats": {
            "total_jobs_in_market": len(jobs_pool),
            "avg_match_score": round(
                sum(j["match_score"] for j in top_matches) / max(len(top_matches), 1), 1
            ),
        },
    })


@app.route("/api/ai/resume/tailor", methods=["POST"])
def tailor_resume():
    """
    Get LLM-generated suggestions for tailoring resume to a specific job.

    Body: {
      "resume_text": str,
      "user_skills": [list],
      "job_id": str   (looked up from DB)
    }
    """
    data = request.json or {}
    resume_text = (data.get("resume_text") or "").strip()
    user_skills = data.get("user_skills", [])
    job_id = data.get("job_id")

    if not resume_text:
        return jsonify({"error": "Missing resume_text"}), 400
    if not job_id:
        return jsonify({"error": "Missing job_id"}), 400
    if not db:
        return jsonify({"error": "Database not configured"}), 503

    # look up the job
    try:
        all_jobs = db.search_jobs(limit=2000)
        job = next((j for j in all_jobs if j.get("job_id") == job_id), None)
    except Exception as e:
        return jsonify({"error": f"Could not fetch job: {e}"}), 500

    if not job:
        return jsonify({"error": "Job not found"}), 404

    # compute match details for this specific job
    scored = job_matcher.score_jobs(user_skills, [job])
    job_with_match = scored[0] if scored else job

    # ask Groq for suggestions
    result = groq.resume_suggestions(
        resume_text=resume_text,
        job_title=job.get("title", ""),
        job_description=job.get("description") or "",
        missing_skills=job_with_match.get("missing_skills", []),
        matched_skills=job_with_match.get("matched_skills", []),
        match_score=job_with_match.get("match_score", 0),
    )

    return jsonify({
        "suggestions": result.get("reply", ""),
        "source": result.get("source", "fallback"),
        "job": {
            "job_id": job.get("job_id"),
            "title": job.get("title"),
            "company": job.get("company"),
            "match_score": job_with_match.get("match_score"),
            "matched_skills": job_with_match.get("matched_skills", []),
            "missing_skills": job_with_match.get("missing_skills", []),
        },
    })


@app.route("/api/ai/chat", methods=["POST"])
def ai_chat():
    """
    Chat with the SkillRadar AI assistant. The LLM gets fresh job market context
    on every call (RAG style) so it answers from your real data.

    Body: {
      "message": str,
      "history": [{role, content}, ...]    (optional)
    }
    """
    data = request.json or {}
    user_message = (data.get("message") or "").strip()
    history = data.get("history", [])

    if not user_message:
        return jsonify({"error": "Empty message"}), 400

    # build context from real data
    context = ""
    try:
        jobs = _get_jobs_for_analysis()
        context = context_builder.build_for_query(user_message, jobs=jobs)
    except Exception as e:
        print(f"[chat] Context build failed: {e}")

    result = groq.chat(
        user_message=user_message,
        context=context,
        history=history,
    )

    return jsonify({
        "reply": result.get("reply", ""),
        "source": result.get("source", "fallback"),
        "context_used": bool(context),
    })


# ---------------- USERS ----------------

@app.route("/api/users/register", methods=["POST"])
def register_user():
    if not db:
        return jsonify({"error": "Database not configured"}), 503
    data = request.json or {}
    email = data.get("email", "").strip().lower()
    if not email:
        return jsonify({"error": "Email required"}), 400
    user = db.create_or_get_user(
        email=email,
        full_name=data.get("full_name", ""),
        college=data.get("college", ""),
    )
    # convert UUID and datetime to strings for JSON
    user["user_id"] = str(user["user_id"])
    for k in ("created_at", "last_login"):
        if user.get(k):
            user[k] = user[k].isoformat() if hasattr(user[k], "isoformat") else str(user[k])
    return jsonify({"user": user})


@app.route("/api/users/<user_id>/saved")
def get_user_saved(user_id: str):
    if not db:
        return jsonify({"error": "Database not configured"}), 503
    jobs = db.get_saved_jobs(user_id)
    return jsonify({"results": jobs})


@app.route("/api/users/<user_id>/save", methods=["POST"])
def save_job(user_id: str):
    if not db:
        return jsonify({"error": "Database not configured"}), 503
    data = request.json or {}
    job_id = data.get("job_id")
    if not job_id:
        return jsonify({"error": "job_id required"}), 400
    db.save_job_for_user(user_id, job_id, notes=data.get("notes", ""))
    return jsonify({"status": "saved"})


@app.route("/api/users/<user_id>/save/<job_id>", methods=["DELETE"])
def unsave_job(user_id: str, job_id: str):
    if not db:
        return jsonify({"error": "Database not configured"}), 503
    db.unsave_job(user_id, job_id)
    return jsonify({"status": "removed"})


# ---------------- helpers ----------------

def _get_jobs_for_analysis() -> list:
    """Get jobs from DB if available, else use fresh search."""
    if db:
        try:
            jobs = db.get_all_jobs(limit=2000)
            if jobs:
                return jobs
        except Exception as e:
            print(f"[DB] Falling back to live data: {e}")

    # fallback: do a live search across common queries
    queries = ["software developer", "data scientist", "python", "react", "java"]
    all_jobs = []
    for q in queries[:2]:    # keep it light if calling live
        results = aggregator.search(query=q, limit=20)
        for j in results:
            if not j.extracted_skills:
                j.extracted_skills = extractor.extract(j.description or "")
        all_jobs.extend([j.to_dict() for j in results])
    return all_jobs


# ---------------- error handlers ----------------

@app.errorhandler(404)
def not_found(e):
    return jsonify({"error": "Endpoint not found"}), 404


@app.errorhandler(500)
def server_error(e):
    return jsonify({"error": "Internal server error", "details": str(e)}), 500


if __name__ == "__main__":
    print(f"Starting SkillRadar API on port {config.PORT}")
    print(f"  Adzuna: {'configured' if adzuna else 'MISSING'}")
    print(f"  Remotive: {'configured' if remotive else 'MISSING'}")
    print(f"  JSearch: {'configured' if jsearch else 'MISSING'}")
    print(f"  Jooble: {'configured' if jooble else 'MISSING'}")
    print(f"  Database: {'connected' if db else 'NOT connected'}")
    print(f"  Groq AI: {'connected' if groq.is_available else 'MISSING (chat will use fallback)'}")
    app.run(host="0.0.0.0", port=config.PORT, debug=config.DEBUG)
