"""
Database layer for SkillRadar.

Wraps Supabase Postgres access. We use psycopg2 directly for queries
because it's simple and the queries we run are straightforward.
"""
import json
import os
from typing import List, Dict, Optional, Any
from contextlib import contextmanager

import psycopg2
from psycopg2.extras import RealDictCursor, Json


class Database:
    def __init__(self, database_url: str):
        self.database_url = database_url

    @contextmanager
    def connection(self):
        """Context manager - opens and closes a connection cleanly."""
        conn = psycopg2.connect(self.database_url)
        try:
            yield conn
            conn.commit()
        except Exception:
            conn.rollback()
            raise
        finally:
            conn.close()

    @contextmanager
    def cursor(self):
        """Cursor context manager that returns dict rows."""
        with self.connection() as conn:
            cur = conn.cursor(cursor_factory=RealDictCursor)
            try:
                yield cur
            finally:
                cur.close()

    # ---------------- JOBS ----------------

    def upsert_job(self, job: dict):
        """Insert or update a job."""
        with self.cursor() as cur:
            cur.execute(
                """
                INSERT INTO jobs (
                    job_id, source, source_url, title, company, location,
                    description, salary_min, salary_max, salary_currency,
                    employment_type, is_remote, posted_date, fetched_at,
                    role_cluster, extracted_skills
                ) VALUES (
                    %(job_id)s, %(source)s, %(source_url)s, %(title)s, %(company)s,
                    %(location)s, %(description)s, %(salary_min)s, %(salary_max)s,
                    %(salary_currency)s, %(employment_type)s, %(is_remote)s,
                    %(posted_date)s, %(fetched_at)s, %(role_cluster)s, %(extracted_skills)s
                )
                ON CONFLICT (job_id) DO UPDATE SET
                    extracted_skills = EXCLUDED.extracted_skills,
                    role_cluster = EXCLUDED.role_cluster,
                    fetched_at = EXCLUDED.fetched_at;
                """,
                {
                    **job,
                    "extracted_skills": Json(job.get("extracted_skills", [])),
                    "posted_date": self._clean_date(job.get("posted_date")),
                    "fetched_at": self._clean_date(job.get("fetched_at")),
                },
            )

    def bulk_upsert_jobs(self, jobs: List[dict]):
        """Insert many jobs in one go. Much faster for batch operations."""
        with self.cursor() as cur:
            for job in jobs:
                cur.execute(
                    """
                    INSERT INTO jobs (
                        job_id, source, source_url, title, company, location,
                        description, salary_min, salary_max, salary_currency,
                        employment_type, is_remote, posted_date, fetched_at,
                        role_cluster, extracted_skills
                    ) VALUES (
                        %(job_id)s, %(source)s, %(source_url)s, %(title)s, %(company)s,
                        %(location)s, %(description)s, %(salary_min)s, %(salary_max)s,
                        %(salary_currency)s, %(employment_type)s, %(is_remote)s,
                        %(posted_date)s, %(fetched_at)s, %(role_cluster)s, %(extracted_skills)s
                    )
                    ON CONFLICT (job_id) DO UPDATE SET
                        extracted_skills = EXCLUDED.extracted_skills,
                        role_cluster = EXCLUDED.role_cluster,
                        fetched_at = EXCLUDED.fetched_at;
                    """,
                    {
                        **job,
                        "extracted_skills": Json(job.get("extracted_skills", [])),
                        "posted_date": self._clean_date(job.get("posted_date")),
                        "fetched_at": self._clean_date(job.get("fetched_at")),
                    },
                )

    def search_jobs(
        self,
        query: Optional[str] = None,
        location: Optional[str] = None,
        skill: Optional[str] = None,
        is_remote: Optional[bool] = None,
        limit: int = 50,
        offset: int = 0,
    ) -> List[Dict]:
        """Search saved jobs by various filters."""
        conditions = []
        params: Dict[str, Any] = {"limit": limit, "offset": offset}

        if query:
            conditions.append(
                "to_tsvector('english', title || ' ' || coalesce(description, '')) @@ plainto_tsquery('english', %(q)s)"
            )
            params["q"] = query
        if location:
            conditions.append("location ILIKE %(loc)s")
            params["loc"] = f"%{location}%"
        if skill:
            conditions.append("extracted_skills ? %(skill)s")
            params["skill"] = skill
        if is_remote is not None:
            conditions.append("is_remote = %(remote)s")
            params["remote"] = is_remote

        where_clause = ("WHERE " + " AND ".join(conditions)) if conditions else ""

        with self.cursor() as cur:
            cur.execute(
                f"""
                SELECT * FROM jobs
                {where_clause}
                ORDER BY posted_date DESC NULLS LAST, fetched_at DESC
                LIMIT %(limit)s OFFSET %(offset)s
                """,
                params,
            )
            return [self._row_to_job(r) for r in cur.fetchall()]

    def count_jobs(self) -> int:
        with self.cursor() as cur:
            cur.execute("SELECT COUNT(*) AS c FROM jobs")
            return cur.fetchone()["c"]

    def get_all_jobs(self, limit: int = 1000) -> List[Dict]:
        """Used by analytics/clustering jobs. Pulls a snapshot."""
        with self.cursor() as cur:
            cur.execute(
                """
                SELECT * FROM jobs
                ORDER BY fetched_at DESC
                LIMIT %s
                """,
                (limit,),
            )
            return [self._row_to_job(r) for r in cur.fetchall()]

    # ---------------- CLUSTERS ----------------

    def save_clusters(self, summary: List[Dict]):
        """Save the latest cluster summary to the DB."""
        with self.cursor() as cur:
            cur.execute("DELETE FROM role_clusters")
            for c in summary:
                cur.execute(
                    """
                    INSERT INTO role_clusters (cluster_id, label, top_skills, job_count)
                    VALUES (%s, %s, %s, %s)
                    """,
                    (c["cluster_id"], c["label"], Json(c["top_skills"]), c["job_count"]),
                )

    def get_clusters(self) -> List[Dict]:
        with self.cursor() as cur:
            cur.execute("SELECT * FROM role_clusters ORDER BY job_count DESC")
            return [dict(r) for r in cur.fetchall()]

    # ---------------- USERS ----------------

    def create_or_get_user(self, email: str, full_name: str = "", college: str = "") -> Dict:
        """Create user if not exists, return user record."""
        with self.cursor() as cur:
            cur.execute(
                """
                INSERT INTO app_users (email, full_name, college)
                VALUES (%s, %s, %s)
                ON CONFLICT (email) DO UPDATE
                    SET last_login = NOW()
                RETURNING *
                """,
                (email, full_name, college),
            )
            return dict(cur.fetchone())

    def save_job_for_user(self, user_id: str, job_id: str, notes: str = ""):
        with self.cursor() as cur:
            cur.execute(
                """
                INSERT INTO saved_jobs (user_id, job_id, notes)
                VALUES (%s, %s, %s)
                ON CONFLICT (user_id, job_id) DO UPDATE SET notes = EXCLUDED.notes
                """,
                (user_id, job_id, notes),
            )

    def get_saved_jobs(self, user_id: str) -> List[Dict]:
        with self.cursor() as cur:
            cur.execute(
                """
                SELECT j.*, sj.saved_at, sj.notes
                FROM saved_jobs sj
                JOIN jobs j ON j.job_id = sj.job_id
                WHERE sj.user_id = %s
                ORDER BY sj.saved_at DESC
                """,
                (user_id,),
            )
            return [self._row_to_job(r) for r in cur.fetchall()]

    def unsave_job(self, user_id: str, job_id: str):
        with self.cursor() as cur:
            cur.execute(
                "DELETE FROM saved_jobs WHERE user_id = %s AND job_id = %s",
                (user_id, job_id),
            )

    # ---------------- helpers ----------------

    def _row_to_job(self, row: dict) -> dict:
        """Convert DB row to clean job dict."""
        d = dict(row)
        # convert datetime objects to strings for JSON compatibility
        for k in ("posted_date", "fetched_at", "saved_at"):
            if k in d and d[k] is not None:
                d[k] = d[k].isoformat() if hasattr(d[k], "isoformat") else str(d[k])
        # extracted_skills might already be a list (from JSONB)
        if isinstance(d.get("extracted_skills"), str):
            try:
                d["extracted_skills"] = json.loads(d["extracted_skills"])
            except json.JSONDecodeError:
                d["extracted_skills"] = []
        return d

    def _clean_date(self, date_str: Optional[str]):
        """Convert ISO string to datetime, return None if invalid."""
        if not date_str:
            return None
        if isinstance(date_str, str):
            from datetime import datetime
            try:
                # try parsing common formats
                for fmt in ["%Y-%m-%dT%H:%M:%S", "%Y-%m-%dT%H:%M:%SZ", "%Y-%m-%dT%H:%M:%S.%f", "%Y-%m-%dT%H:%M:%S.%fZ", "%Y-%m-%d"]:
                    try:
                        return datetime.strptime(date_str[:26], fmt)
                    except ValueError:
                        continue
                return None
            except (ValueError, TypeError):
                return None
        return date_str
