"""
Trend Analysis Module.

Once we have skills extracted from jobs (with timestamps), we can analyze:
  - Most frequent skills overall
  - Fast growing skills (high week over week growth)
  - Emerging skills (low base count but rising fast)
  - Declining skills (negative growth)

This is what powers the analytics dashboard.
"""
from collections import Counter, defaultdict
from datetime import datetime, timedelta
from typing import List, Dict, Optional
import statistics


class TrendAnalyzer:
    def __init__(self):
        pass

    def top_skills(self, jobs: List[dict], top_n: int = 20) -> List[Dict]:
        """
        Most frequently demanded skills across all jobs.

        Args:
            jobs: list of dicts with 'extracted_skills' field (list of skill names)
            top_n: how many top skills to return

        Returns:
            list of {skill, count, percentage} dicts
        """
        skill_counter = Counter()
        total_jobs = len(jobs)

        for job in jobs:
            # use set so each job counts a skill at most once
            for skill in set(job.get("extracted_skills", [])):
                skill_counter[skill] += 1

        results = []
        for skill, count in skill_counter.most_common(top_n):
            results.append({
                "skill": skill,
                "count": count,
                "percentage": round((count / total_jobs * 100), 2) if total_jobs else 0,
            })
        return results

    def skill_growth(
        self,
        jobs: List[dict],
        window_days: int = 7,
        compare_with_days: int = 14,
    ) -> List[Dict]:
        """
        Calculate growth rate for each skill.

        Compares the last `window_days` vs the previous `compare_with_days` period.

        Returns:
            list of {skill, recent_count, previous_count, growth_rate} sorted by growth
        """
        now = datetime.now()
        recent_cutoff = now - timedelta(days=window_days)
        previous_cutoff = now - timedelta(days=window_days + compare_with_days)

        recent_counter = Counter()
        previous_counter = Counter()

        for job in jobs:
            posted_at = self._parse_date(job.get("posted_date") or job.get("fetched_at"))
            if not posted_at:
                continue

            skills = set(job.get("extracted_skills", []))

            if posted_at >= recent_cutoff:
                for s in skills:
                    recent_counter[s] += 1
            elif posted_at >= previous_cutoff:
                for s in skills:
                    previous_counter[s] += 1

        # combine all unique skills
        all_skills = set(recent_counter) | set(previous_counter)

        results = []
        for skill in all_skills:
            recent = recent_counter[skill]
            previous = previous_counter[skill]

            # calculate growth rate (handle div by zero)
            if previous == 0:
                if recent >= 3:
                    growth = 999.0   # "infinite" growth - brand new trending skill
                else:
                    growth = 0
            else:
                growth = round(((recent - previous) / previous) * 100, 1)

            results.append({
                "skill": skill,
                "recent_count": recent,
                "previous_count": previous,
                "growth_rate": growth,
            })

        # sort by growth rate descending
        results.sort(key=lambda x: x["growth_rate"], reverse=True)
        return results

    def trending_skills(
        self,
        jobs: List[dict],
        top_n: int = 15,
        min_count: int = 5,
    ) -> List[Dict]:
        """
        Skills that are growing AND have meaningful volume.
        Filters out noise from skills that just bounced from 1 to 2 mentions.
        """
        growth = self.skill_growth(jobs)
        # keep only skills with enough total mentions
        filtered = [
            g for g in growth
            if (g["recent_count"] + g["previous_count"]) >= min_count
            and g["growth_rate"] > 0
        ]
        return filtered[:top_n]

    def emerging_skills(
        self,
        jobs: List[dict],
        top_n: int = 10,
    ) -> List[Dict]:
        """
        Skills with low/zero previous count but recent activity.
        These are 'new on the radar' kind of skills.
        """
        growth = self.skill_growth(jobs)
        emerging = [
            g for g in growth
            if g["previous_count"] <= 2 and g["recent_count"] >= 3
        ]
        emerging.sort(key=lambda x: x["recent_count"], reverse=True)
        return emerging[:top_n]

    def declining_skills(
        self,
        jobs: List[dict],
        top_n: int = 10,
        min_previous: int = 5,
    ) -> List[Dict]:
        """Skills with negative growth and previously had real volume."""
        growth = self.skill_growth(jobs)
        declining = [
            g for g in growth
            if g["previous_count"] >= min_previous and g["growth_rate"] < -20
        ]
        declining.sort(key=lambda x: x["growth_rate"])
        return declining[:top_n]

    def category_distribution(self, jobs: List[dict]) -> Dict[str, int]:
        """
        How many jobs require skills from each category?
        Useful for the pie chart on the dashboard.
        """
        from .skill_taxonomy import get_category   # local import to avoid circular

        category_counts = Counter()
        for job in jobs:
            categories = set()
            for skill in job.get("extracted_skills", []):
                categories.add(get_category(skill))
            for cat in categories:
                category_counts[cat] += 1
        return dict(category_counts.most_common())

    def _parse_date(self, date_str: Optional[str]) -> Optional[datetime]:
        """Parse various date formats we might get from different APIs."""
        if not date_str:
            return None
        if isinstance(date_str, datetime):
            return date_str

        formats = [
            "%Y-%m-%dT%H:%M:%S",
            "%Y-%m-%dT%H:%M:%SZ",
            "%Y-%m-%dT%H:%M:%S.%f",
            "%Y-%m-%dT%H:%M:%S.%fZ",
            "%Y-%m-%d %H:%M:%S",
            "%Y-%m-%d",
        ]
        for fmt in formats:
            try:
                return datetime.strptime(date_str[:26], fmt)
            except (ValueError, TypeError):
                continue
        return None


# convenience singleton
_default_analyzer = None


def get_analyzer() -> TrendAnalyzer:
    global _default_analyzer
    if _default_analyzer is None:
        _default_analyzer = TrendAnalyzer()
    return _default_analyzer
