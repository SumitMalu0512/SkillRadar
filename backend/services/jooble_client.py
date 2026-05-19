"""
Jooble API client.

Jooble aggregates job listings from across the web - thousands of job boards
worldwide including Indian portals. Free tier with generous rate limits.

Docs: https://jooble.org/api/about
Auth: POST request with API key in URL path

Adds another solid source to our job aggregator alongside Adzuna, Remotive, JSearch.
"""
import requests
import hashlib
import re
from typing import List, Optional
from .job_model import JobPosting


class JoobleClient:
    """
    Jooble uses POST requests with JSON body, key embedded in URL path.
    URL pattern: https://jooble.org/api/{API_KEY}
    """
    BASE_URL = "https://jooble.org/api"

    def __init__(self, api_key: str, cache=None):
        self.api_key = api_key
        self.cache = cache

    def search(
        self,
        query: str = "",
        location: str = "India",
        page: int = 1,
        results_per_page: int = 20,
        remote_only: bool = False,
    ) -> List[JobPosting]:
        """
        Search Jooble for jobs matching the query.
        Returns up to results_per_page postings normalized as JobPosting objects.
        """
        if not self.api_key:
            return []

        # check cache first
        cache_key = self._cache_key(query, location, page, results_per_page, remote_only)
        if self.cache:
            cached = self.cache.get(cache_key)
            if cached is not None:
                return [JobPosting.from_dict(d) for d in cached]

        # Jooble uses "Remote" as a location to filter remote-only roles
        loc = "Remote" if remote_only else location

        payload = {
            "keywords": query or "",
            "location": loc,
            "page": str(page),
            "ResultOnPage": str(results_per_page),
        }

        try:
            resp = requests.post(
                f"{self.BASE_URL}/{self.api_key}",
                json=payload,
                headers={"Content-Type": "application/json"},
                timeout=15,
            )
            if resp.status_code != 200:
                print(f"[Jooble] HTTP {resp.status_code}: {resp.text[:200]}")
                return []
            data = resp.json()
        except requests.RequestException as e:
            print(f"[Jooble] Request failed: {e}")
            return []
        except ValueError as e:
            print(f"[Jooble] Bad JSON: {e}")
            return []

        jobs = []
        for item in data.get("jobs", []):
            job = self._normalize(item)
            if job:
                jobs.append(job)

        if self.cache and jobs:
            self.cache.set(cache_key, [j.to_dict() for j in jobs])

        return jobs

    def _normalize(self, item: dict) -> Optional[JobPosting]:
        """Convert a Jooble job dict into our standard JobPosting model."""
        try:
            url = item.get("link", "")
            source_id = item.get("id") or hashlib.md5(url.encode()).hexdigest()[:16]

            title = (item.get("title") or "").strip()
            company = (item.get("company") or "Unknown").strip()
            description = (item.get("snippet") or "").strip()

            # detect remote from title or snippet
            text_blob = f"{title} {description}".lower()
            is_remote = any(w in text_blob for w in ["remote", "work from home", "wfh"])

            sal_min, sal_max, sal_currency = self._parse_salary(item.get("salary", ""))

            return JobPosting(
                job_id=f"jooble_{source_id}",
                title=title,
                company=company,
                location=(item.get("location") or "").strip(),
                description=description,
                source_url=url,
                source="jooble",
                posted_date=item.get("updated"),
                is_remote=is_remote,
                salary_min=sal_min,
                salary_max=sal_max,
                salary_currency=sal_currency,
            )
        except Exception as e:
            print(f"[Jooble] Failed to normalize job: {e}")
            return None

    def _parse_salary(self, salary_str: str):
        """
        Jooble returns salary as free-form text like '$50,000 - $80,000'
        or '₹5L - ₹10L'. Best-effort extraction.
        """
        if not salary_str:
            return None, None, None

        currency = "USD"
        if "₹" in salary_str or "INR" in salary_str.upper():
            currency = "INR"
        elif "€" in salary_str or "EUR" in salary_str.upper():
            currency = "EUR"
        elif "£" in salary_str or "GBP" in salary_str.upper():
            currency = "GBP"

        numbers = re.findall(r"\d+(?:\.\d+)?", salary_str.replace(",", ""))
        try:
            nums = [float(n) for n in numbers if n]
        except ValueError:
            return None, None, currency

        if len(nums) >= 2:
            return nums[0], nums[1], currency
        elif len(nums) == 1:
            return nums[0], nums[0], currency
        return None, None, currency

    def _cache_key(self, q, loc, page, n, remote):
        raw = f"jooble:{q}:{loc}:{page}:{n}:{remote}"
        return hashlib.md5(raw.encode()).hexdigest()
