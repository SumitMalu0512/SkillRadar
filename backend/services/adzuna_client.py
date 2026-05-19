"""
Adzuna API client.

Adzuna gives us solid coverage of Indian job market - they aggregate
from Naukri network, TimesJobs, and many smaller Indian job boards.
Free tier: 250 calls/month which is plenty for our project.

Docs: https://developer.adzuna.com/docs/search
"""
import requests
import hashlib
from typing import List, Optional
from .job_model import JobPosting


class AdzunaClient:
    BASE_URL = "https://api.adzuna.com/v1/api/jobs"

    def __init__(self, app_id: str, app_key: str, cache=None):
        self.app_id = app_id
        self.app_key = app_key
        self.cache = cache

    def search(
        self,
        query: str = "",
        location: str = "",
        country: str = "in",   # india by default
        page: int = 1,
        results_per_page: int = 20,
    ) -> List[JobPosting]:
        """Search jobs on Adzuna. Returns list of normalized JobPosting objects."""

        cache_key = f"adzuna:{country}:{query}:{location}:{page}:{results_per_page}"

        # check cache first
        if self.cache:
            cached = self.cache.get(cache_key)
            if cached is not None:
                return [JobPosting(**j) for j in cached]

        url = f"{self.BASE_URL}/{country}/search/{page}"
        params = {
            "app_id": self.app_id,
            "app_key": self.app_key,
            "results_per_page": results_per_page,
            "content-type": "application/json",
        }
        if query:
            params["what"] = query
        if location:
            params["where"] = location

        try:
            resp = requests.get(url, params=params, timeout=15)
            resp.raise_for_status()
            data = resp.json()
        except requests.RequestException as e:
            print(f"[Adzuna] Request failed: {e}")
            return []

        jobs = []
        for item in data.get("results", []):
            try:
                job = self._parse_job(item)
                jobs.append(job)
            except Exception as e:
                # if one job fails to parse, skip it - don't kill the whole batch
                print(f"[Adzuna] Failed to parse job: {e}")
                continue

        # cache the result
        if self.cache:
            self.cache.set(cache_key, [j.to_dict() for j in jobs])

        return jobs

    def _parse_job(self, item: dict) -> JobPosting:
        # adzuna's id is a long number - we prefix it so it never collides
        raw_id = str(item.get("id", ""))
        job_id = f"adzuna_{raw_id}" if raw_id else self._generate_id(item)

        return JobPosting(
            job_id=job_id,
            source="adzuna",
            source_url=item.get("redirect_url", ""),
            title=item.get("title", "Untitled").strip(),
            company=item.get("company", {}).get("display_name", "Unknown"),
            location=item.get("location", {}).get("display_name", ""),
            description=item.get("description", ""),
            salary_min=item.get("salary_min"),
            salary_max=item.get("salary_max"),
            salary_currency="INR",
            employment_type=item.get("contract_time"),
            is_remote=False,  # adzuna doesn't reliably mark remote
            posted_date=item.get("created"),
        )

    def _generate_id(self, item: dict) -> str:
        # fallback: hash title + company so we get a stable ID
        key = f"{item.get('title', '')}-{item.get('company', {}).get('display_name', '')}"
        return f"adzuna_{hashlib.md5(key.encode()).hexdigest()[:12]}"
