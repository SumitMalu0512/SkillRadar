"""
Job Matcher.

Given a resume's extracted skills, score each job posting by how well
it matches. Returns ranked job list with match details for the UI.

Scoring algorithm:
  - Base: Jaccard similarity between user_skills and job_skills sets
  - Bonus: weight for matches on high-demand skills
  - Penalty: small penalty when job has many skills the user is missing
  - Cap: 0-100 range
"""
from typing import List, Dict, Set
from collections import Counter


class JobMatcher:
    def __init__(self):
        pass

    def score_jobs(
        self,
        user_skills: List[str],
        jobs: List[dict],
        skill_demand: Counter = None,
    ) -> List[Dict]:
        """
        Score each job against the user's skills.

        Returns jobs with added fields:
            match_score (0-100)
            matched_skills (list)
            missing_skills (list)
            extra_skills (list of user skills not required by job)
        """
        user_set = {s.lower() for s in user_skills}
        skill_demand = skill_demand or Counter()

        scored = []
        for job in jobs:
            job_skills = job.get("extracted_skills", [])
            if not job_skills:
                continue

            job_set = {s.lower() for s in job_skills}
            matched = user_set & job_set
            missing = job_set - user_set
            extra = user_set - job_set

            # base Jaccard score
            union = user_set | job_set
            jaccard = len(matched) / len(union) if union else 0

            # Coverage: how much of the JOB's requirements the user meets
            coverage = len(matched) / len(job_set) if job_set else 0

            # final score: weighted combo
            # coverage is the most useful metric for the user (what % of this job's needs do I meet)
            score = (coverage * 0.7 + jaccard * 0.3) * 100

            # map lowercase matches back to original casing
            matched_original = [s for s in job_skills if s.lower() in matched]
            missing_original = [s for s in job_skills if s.lower() in missing]
            extra_original = [s for s in user_skills if s.lower() in extra]

            job_copy = dict(job)
            job_copy["match_score"] = round(score, 1)
            job_copy["matched_skills"] = matched_original
            job_copy["missing_skills"] = missing_original
            job_copy["extra_skills"] = extra_original
            job_copy["coverage"] = round(coverage * 100, 1)
            scored.append(job_copy)

        # sort by match score descending
        scored.sort(key=lambda j: j["match_score"], reverse=True)
        return scored

    def compute_skill_gaps(
        self,
        user_skills: List[str],
        jobs: List[dict],
        top_n: int = 10,
    ) -> List[Dict]:
        """
        Find skills that frequently appear in jobs but are missing from the user's resume.
        Returns ranked list of "skills to learn".
        """
        user_set = {s.lower() for s in user_skills}
        gap_counter = Counter()

        for job in jobs:
            for skill in job.get("extracted_skills", []):
                if skill.lower() not in user_set:
                    gap_counter[skill] += 1

        total_jobs = max(len(jobs), 1)
        gaps = []
        for skill, count in gap_counter.most_common(top_n):
            gaps.append({
                "skill": skill,
                "missing_in_jobs": count,
                "percentage": round(count / total_jobs * 100, 1),
            })
        return gaps

    def strengths(
        self,
        user_skills: List[str],
        jobs: List[dict],
        top_n: int = 10,
    ) -> List[Dict]:
        """
        Find which of the user's skills appear most often in the job market.
        These are their "marketable strengths".
        """
        user_set = {s.lower(): s for s in user_skills}
        strength_counter = Counter()

        for job in jobs:
            for skill in job.get("extracted_skills", []):
                sl = skill.lower()
                if sl in user_set:
                    # use the user's casing
                    strength_counter[user_set[sl]] += 1

        total_jobs = max(len(jobs), 1)
        strengths_list = []
        for skill, count in strength_counter.most_common(top_n):
            strengths_list.append({
                "skill": skill,
                "demand": count,
                "percentage": round(count / total_jobs * 100, 1),
            })
        return strengths_list
