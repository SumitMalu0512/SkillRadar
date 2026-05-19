-- SkillRadar Database Schema
-- Run this in Supabase SQL Editor: https://supabase.com/dashboard/project/_/sql

-- ============================================================
-- 1. JOBS table - stores all fetched job postings
-- ============================================================
CREATE TABLE IF NOT EXISTS jobs (
    job_id          TEXT PRIMARY KEY,
    source          TEXT NOT NULL,                  -- adzuna / remotive / jsearch
    source_url      TEXT,
    title           TEXT NOT NULL,
    company         TEXT,
    location        TEXT,
    description     TEXT,
    salary_min      NUMERIC,
    salary_max      NUMERIC,
    salary_currency TEXT,
    employment_type TEXT,
    is_remote       BOOLEAN DEFAULT FALSE,
    posted_date     TIMESTAMP,
    fetched_at      TIMESTAMP DEFAULT NOW(),
    role_cluster    INTEGER,
    extracted_skills JSONB DEFAULT '[]'::jsonb
);

CREATE INDEX IF NOT EXISTS idx_jobs_source ON jobs(source);
CREATE INDEX IF NOT EXISTS idx_jobs_company ON jobs(company);
CREATE INDEX IF NOT EXISTS idx_jobs_posted_date ON jobs(posted_date DESC);
CREATE INDEX IF NOT EXISTS idx_jobs_is_remote ON jobs(is_remote);
CREATE INDEX IF NOT EXISTS idx_jobs_cluster ON jobs(role_cluster);
CREATE INDEX IF NOT EXISTS idx_jobs_skills_gin ON jobs USING GIN (extracted_skills);

-- Full text search index for job title + description
CREATE INDEX IF NOT EXISTS idx_jobs_search
    ON jobs USING GIN (to_tsvector('english', title || ' ' || coalesce(description, '')));

-- ============================================================
-- 2. SKILL_TRENDS - daily aggregated skill mention counts
-- ============================================================
CREATE TABLE IF NOT EXISTS skill_trends (
    id              BIGSERIAL PRIMARY KEY,
    skill_name      TEXT NOT NULL,
    skill_category  TEXT,
    snapshot_date   DATE NOT NULL,
    job_count       INTEGER DEFAULT 0,
    UNIQUE (skill_name, snapshot_date)
);

CREATE INDEX IF NOT EXISTS idx_trends_skill ON skill_trends(skill_name);
CREATE INDEX IF NOT EXISTS idx_trends_date ON skill_trends(snapshot_date DESC);

-- ============================================================
-- 3. ROLE_CLUSTERS - K-Means cluster definitions
-- ============================================================
CREATE TABLE IF NOT EXISTS role_clusters (
    cluster_id      INTEGER PRIMARY KEY,
    label           TEXT NOT NULL,
    top_skills      JSONB,
    job_count       INTEGER DEFAULT 0,
    last_updated    TIMESTAMP DEFAULT NOW()
);

-- ============================================================
-- 4. SKILL_FORECASTS - Prophet output stored per skill
-- ============================================================
CREATE TABLE IF NOT EXISTS skill_forecasts (
    id              BIGSERIAL PRIMARY KEY,
    skill_name      TEXT NOT NULL,
    forecast_date   DATE NOT NULL,
    predicted_demand NUMERIC,
    lower_bound     NUMERIC,
    upper_bound     NUMERIC,
    generated_at    TIMESTAMP DEFAULT NOW(),
    UNIQUE (skill_name, forecast_date)
);

CREATE INDEX IF NOT EXISTS idx_forecasts_skill ON skill_forecasts(skill_name);

-- ============================================================
-- 5. USERS - for login & saved jobs feature
-- ============================================================
CREATE TABLE IF NOT EXISTS app_users (
    user_id         UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    email           TEXT UNIQUE NOT NULL,
    full_name       TEXT,
    college         TEXT,
    target_role     TEXT,
    created_at      TIMESTAMP DEFAULT NOW(),
    last_login      TIMESTAMP
);

-- ============================================================
-- 6. SAVED_JOBS - jobs bookmarked by users
-- ============================================================
CREATE TABLE IF NOT EXISTS saved_jobs (
    id              BIGSERIAL PRIMARY KEY,
    user_id         UUID REFERENCES app_users(user_id) ON DELETE CASCADE,
    job_id          TEXT REFERENCES jobs(job_id) ON DELETE CASCADE,
    saved_at        TIMESTAMP DEFAULT NOW(),
    notes           TEXT,
    UNIQUE (user_id, job_id)
);

CREATE INDEX IF NOT EXISTS idx_saved_user ON saved_jobs(user_id);

-- ============================================================
-- 7. USER_SKILLS - what skills the user already has (for gap analysis)
-- ============================================================
CREATE TABLE IF NOT EXISTS user_skills (
    id              BIGSERIAL PRIMARY KEY,
    user_id         UUID REFERENCES app_users(user_id) ON DELETE CASCADE,
    skill_name      TEXT NOT NULL,
    proficiency     TEXT,            -- beginner / intermediate / advanced
    added_at        TIMESTAMP DEFAULT NOW(),
    UNIQUE (user_id, skill_name)
);

-- ============================================================
-- DONE - verify with these queries
-- ============================================================
-- SELECT count(*) FROM jobs;
-- SELECT count(*) FROM skill_trends;
-- SELECT * FROM role_clusters;
