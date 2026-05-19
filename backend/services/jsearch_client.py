"""
JSearch API client (via RapidAPI).

JSearch is the big one - it pulls real time data from LinkedIn, Indeed,
Glassdoor, ZipRecruiter, Google for Jobs. This is what lets us claim
coverage of all major job portals.

Free tier: 200 requests/month. We cache aggressively.

Docs: https://rapidapi.com/letscrape-6bRBa3QguO5/api/jsearch
"""
import requests
import hashlib
from typing import List, Optional
from .job_model import JobPosting


class JSearchClient:
    BASE_URL = "https://jsearch.p.rapidapi.com/search"

    def __init__(self, rapidapi_key: str, cache=None):
        self.api_key = rapidapi_key
        self.cache = cache

    def search(
        self,
        query: str = "software developer",
        location: str = "India",
        page: int = 1,
        num_pages: int = 1,
        employment_type: Optional[str] = None,
        remote_only: bool = False,
        date_posted: str = "month",   # all, today, 3days, week, month
    ) -> List[JobPosting]:
        """Search jobs aggregated from LinkedIn, Indeed, Glassdoor etc."""

        # build the actual query string jsearch expects
        full_query = f"{query} in {location}" if location else query

        cache_key = f"jsearch:{full_query}:{page}:{num_pages}:{employment_type}:{remote_only}:{date_posted}"

        if self.cache:
            cached = self.cache.get(cache_key)
            if cached is not None:
                return [JobPosting(**j) for j in cached]

        params = {
            "query": full_query,
            "page": str(page),
            "num_pages": str(num_pages),
            "date_posted": date_posted,
        }
        if employment_type:
            params["employment_types"] = employment_type.upper()
        if remote_only:
            params["work_from_home"] = "true"

        headers = {
            "X-RapidAPI-Key": self.api_key,
            "X-RapidAPI-Host": "jsearch.p.rapidapi.com",
        }

        try:
            resp = requests.get(self.BASE_URL, params=params, headers=headers, timeout=20)
            resp.raise_for_status()
            data = resp.json()
        except requests.RequestException as e:
            print(f"[JSearch] Request failed: {e}")
            return []

        jobs = []
        for item in data.get("data", []):
            try:
                jobs.append(self._parse_job(item))
            except Exception as e:
                print(f"[JSearch] Parse error: {e}")
                continue

        if self.cache:
            self.cache.set(cache_key, [j.to_dict() for j in jobs])

        return jobs

    def _parse_job(self, item: dict) -> JobPosting:
        raw_id = item.get("job_id", "")
        job_id = f"jsearch_{raw_id}" if raw_id else self._generate_id(item)

        # build a location string from the pieces jsearch gives us
        loc_parts = []
        if item.get("job_city"):
            loc_parts.append(item["job_city"])
        if item.get("job_state"):
            loc_parts.append(item["job_state"])
        if item.get("job_country"):
            loc_parts.append(item["job_country"])
        location = ", ".join(loc_parts) if loc_parts else "Not specified"

        return JobPosting(
            job_id=job_id,
            source="jsearch",
            source_url=item.get("job_apply_link", ""),
            title=item.get("job_title", "Untitled").strip(),
            company=item.get("employer_name", "Unknown"),
            location=location,
            description=item.get("job_description", ""),
            salary_min=item.get("job_min_salary"),
            salary_max=item.get("job_max_salary"),
            salary_currency=item.get("job_salary_currency"),
            employment_type=item.get("job_employment_type"),
            is_remote=bool(item.get("job_is_remote", False)),
            posted_date=item.get("job_posted_at_datetime_utc"),
        )

    def _generate_id(self, item: dict) -> str:
        key = f"{item.get('job_title', '')}-{item.get('employer_name', '')}"
        return f"jsearch_{hashlib.md5(key.encode()).hexdigest()[:12]}"
