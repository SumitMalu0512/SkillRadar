"""
Master job aggregator.

This is the main entry point. It calls all configured job APIs in parallel,
deduplicates, and returns a single clean list of jobs.

Why parallel? Waiting for 4 APIs sequentially would be slow (15+ seconds).
With ThreadPoolExecutor it's ~5 seconds max.
"""
from concurrent.futures import ThreadPoolExecutor, as_completed
from typing import List, Optional
import hashlib

from .job_model import JobPosting


class JobAggregator:
    def __init__(self, adzuna=None, remotive=None, jsearch=None, jooble=None):
        # any of these can be None - we just skip that source
        self.adzuna = adzuna
        self.remotive = remotive
        self.jsearch = jsearch
        self.jooble = jooble

    def search(
        self,
        query: str = "",
        location: str = "India",
        remote_only: bool = False,
        limit: int = 200,
    ) -> List[JobPosting]:
        """
        Search across all configured job sources in parallel.
        Returns deduplicated, merged list of jobs.
        """
        tasks = []

        with ThreadPoolExecutor(max_workers=4) as executor:
            if self.adzuna and not remote_only:
                # adzuna doesn't really do remote so skip it for remote-only searches
                tasks.append(
                    executor.submit(
                        self._safe_call,
                        "adzuna",
                        self.adzuna.search,
                        query=query,
                        location=location,
                        results_per_page=50,    # Adzuna max
                    )
                )

            if self.remotive:
                tasks.append(
                    executor.submit(
                        self._safe_call,
                        "remotive",
                        self.remotive.search,
                        query=query,
                        limit=100,    # Remotive returns all matching - pull a lot
                    )
                )

            if self.jsearch:
                tasks.append(
                    executor.submit(
                        self._safe_call,
                        "jsearch",
                        self.jsearch.search,
                        query=query or "software developer",
                        location=location,
                        remote_only=remote_only,
                        num_pages=2,   # JSearch: 10 per page, so 2 pages = ~20 jobs
                    )
                )

            if self.jooble:
                tasks.append(
                    executor.submit(
                        self._safe_call,
                        "jooble",
                        self.jooble.search,
                        query=query or "developer",
                        location=location if not remote_only else "",
                        results_per_page=50,    # Jooble max
                    )
                )

            all_jobs = []
            for future in as_completed(tasks):
                jobs = future.result()
                all_jobs.extend(jobs)

        # dedupe and limit
        deduped = self._deduplicate(all_jobs)

        # if remote_only and the source didn't filter, do it ourselves
        if remote_only:
            deduped = [j for j in deduped if j.is_remote]

        return deduped[:limit]

    def _safe_call(self, source_name: str, fn, **kwargs) -> List[JobPosting]:
        """Wrap each API call so one failure doesn't kill all results."""
        try:
            jobs = fn(**kwargs)
            print(f"[{source_name}] fetched {len(jobs)} jobs")
            return jobs
        except Exception as e:
            print(f"[{source_name}] FAILED: {e}")
            return []

    def _deduplicate(self, jobs: List[JobPosting]) -> List[JobPosting]:
        """
        Remove duplicate jobs that appear on multiple portals.
        We dedupe by (title + company + location) signature.
        """
        seen = set()
        unique = []
        for job in jobs:
            sig = self._signature(job)
            if sig not in seen:
                seen.add(sig)
                unique.append(job)
        return unique

    def _signature(self, job: JobPosting) -> str:
        # normalize so casing/whitespace doesn't matter
        title = job.title.lower().strip()
        company = job.company.lower().strip()
        location = (job.location or "").lower().strip()
        key = f"{title}|{company}|{location}"
        return hashlib.md5(key.encode()).hexdigest()

    def stats(self, jobs: List[JobPosting]) -> dict:
        """Quick summary of what we got - useful for the UI."""
        by_source = {}
        for j in jobs:
            by_source[j.source] = by_source.get(j.source, 0) + 1
        return {
            "total": len(jobs),
            "by_source": by_source,
            "remote_count": sum(1 for j in jobs if j.is_remote),
            "with_salary": sum(1 for j in jobs if j.has_salary),
        }
