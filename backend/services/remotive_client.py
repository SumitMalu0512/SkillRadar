"""
Remotive API client.

Remotive curates remote jobs from companies worldwide. No API key needed,
no rate limit (within reason). Great for tech / remote coverage.

Docs: https://remotive.com/api-documentation
"""
import requests
import hashlib
from typing import List
from .job_model import JobPosting


class RemotiveClient:
    BASE_URL = "https://remotive.com/api/remote-jobs"

    # remotive categories we care about for a tech-focused project
    TECH_CATEGORIES = [
        "software-dev",
        "data",
        "devops",
        "qa",
        "design",
        "product",
    ]

    def __init__(self, cache=None):
        self.cache = cache

    def search(self, query: str = "", category: str = "", limit: int = 50) -> List[JobPosting]:
        """
        Search remote jobs.
        Note: Remotive doesn't have a location filter (it's all remote by definition).
        """
        cache_key = f"remotive:{query}:{category}:{limit}"

        if self.cache:
            cached = self.cache.get(cache_key)
            if cached is not None:
                return [JobPosting(**j) for j in cached]

        params = {"limit": limit}
        if query:
            params["search"] = query
        if category:
            params["category"] = category

        try:
            resp = requests.get(self.BASE_URL, params=params, timeout=15)
            resp.raise_for_status()
            data = resp.json()
        except requests.RequestException as e:
            print(f"[Remotive] Request failed: {e}")
            return []

        jobs = []
        for item in data.get("jobs", []):
            try:
                jobs.append(self._parse_job(item))
            except Exception as e:
                print(f"[Remotive] Failed to parse: {e}")
                continue

        if self.cache:
            self.cache.set(cache_key, [j.to_dict() for j in jobs])

        return jobs

    def _parse_job(self, item: dict) -> JobPosting:
        raw_id = str(item.get("id", ""))
        job_id = f"remotive_{raw_id}" if raw_id else self._generate_id(item)

        # remotive sometimes gives salary as a string like "$50000 - $70000"
        # we don't parse it here - too messy. We'll handle it later if needed.
        return JobPosting(
            job_id=job_id,
            source="remotive",
            source_url=item.get("url", ""),
            title=item.get("title", "Untitled").strip(),
            company=item.get("company_name", "Unknown"),
            location=item.get("candidate_required_location", "Remote"),
            description=item.get("description", ""),
            employment_type=item.get("job_type"),
            is_remote=True,    # everything on remotive is remote
            posted_date=item.get("publication_date"),
        )

    def _generate_id(self, item: dict) -> str:
        key = f"{item.get('title', '')}-{item.get('company_name', '')}"
        return f"remotive_{hashlib.md5(key.encode()).hexdigest()[:12]}"
