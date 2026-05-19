"""
RAG Context Builder.

Builds a compact text context from the job market database to feed
into the LLM. This is what makes our chat "know" the live data
rather than just hallucinating.
"""
from collections import Counter
from typing import List, Dict, Optional


class ContextBuilder:
    def __init__(self, db=None, analyzer=None):
        self.db = db
        self.analyzer = analyzer

    def build_for_query(self, user_query: str, jobs: List[dict] = None) -> str:
        """
        Build a context block based on what the user is asking about.
        Returns a compact text representation suitable for LLM context.
        """
        q = user_query.lower()
        parts = []

        if jobs is None:
            jobs = self._get_jobs()

        if not jobs:
            return "No job market data is currently available in the database."

        parts.append(f"Job market snapshot: {len(jobs)} active job postings analyzed.")

        # always include top skills - useful for almost any query
        top_skills = self.analyzer.top_skills(jobs, top_n=15) if self.analyzer else []
        if top_skills:
            top_lines = [f"- {s['skill']}: {s['count']} jobs ({s['percentage']}%)" for s in top_skills[:10]]
            parts.append("Top 10 most demanded skills:\n" + "\n".join(top_lines))

        # if user asked about trends, add trend data
        if any(w in q for w in ["trend", "trending", "popular", "growing", "rising", "hot"]):
            trending = self.analyzer.trending_skills(jobs, top_n=8) if self.analyzer else []
            if trending:
                t_lines = [
                    f"- {s['skill']}: +{s['growth_rate']}% growth (recent: {s['recent_count']}, previous: {s['previous_count']})"
                    for s in trending[:6]
                ]
                parts.append("Fastest growing skills:\n" + "\n".join(t_lines))

        # if user asked about declining, add that
        if any(w in q for w in ["decline", "falling", "dying", "obsolete", "outdated"]):
            declining = self.analyzer.declining_skills(jobs, top_n=5) if self.analyzer else []
            if declining:
                d_lines = [f"- {s['skill']}: {s['growth_rate']}% change" for s in declining[:5]]
                parts.append("Declining skills:\n" + "\n".join(d_lines))

        # if user asked about emerging
        if any(w in q for w in ["new", "emerging", "appearing", "fresh"]):
            emerging = self.analyzer.emerging_skills(jobs, top_n=5) if self.analyzer else []
            if emerging:
                e_lines = [f"- {s['skill']}: appearing in {s['recent_count']} recent posts" for s in emerging[:5]]
                parts.append("Emerging skills (newly appearing):\n" + "\n".join(e_lines))

        # categories - useful for high-level questions
        if any(w in q for w in ["category", "categories", "field", "domain", "area"]):
            cats = self.analyzer.category_distribution(jobs) if self.analyzer else {}
            if cats:
                c_lines = [f"- {k}: {v} jobs" for k, v in list(cats.items())[:8]]
                parts.append("Job distribution by category:\n" + "\n".join(c_lines))

        # location stats
        if any(w in q for w in ["location", "city", "where", "remote", "pune", "bangalore", "mumbai", "delhi"]):
            loc_counter = Counter()
            for j in jobs:
                loc = (j.get("location") or "").strip()
                if loc:
                    loc_counter[loc] += 1
            if loc_counter:
                l_lines = [f"- {loc}: {count} jobs" for loc, count in loc_counter.most_common(8)]
                parts.append("Top job locations:\n" + "\n".join(l_lines))
            remote_count = sum(1 for j in jobs if j.get("is_remote"))
            parts.append(f"Remote jobs available: {remote_count} ({round(remote_count/len(jobs)*100)}% of total)")

        # company info
        if any(w in q for w in ["company", "companies", "employer", "hiring"]):
            comp_counter = Counter()
            for j in jobs:
                c = (j.get("company") or "").strip()
                if c and c.lower() != "unknown":
                    comp_counter[c] += 1
            if comp_counter:
                c_lines = [f"- {c}: {n} openings" for c, n in comp_counter.most_common(8)]
                parts.append("Top hiring companies:\n" + "\n".join(c_lines))

        # specific skill mentioned
        for word in user_query.split():
            if len(word) >= 3:
                matches = self._find_skill_matches(word, jobs)
                if matches:
                    parts.append(f"Data about '{word}':\n" + matches)

        return "\n\n".join(parts)

    def _find_skill_matches(self, query_word: str, jobs: List[dict]) -> Optional[str]:
        """If the user mentions a specific skill, pull stats about it."""
        q = query_word.lower().strip(".,!?")
        if len(q) < 3:
            return None

        # find jobs that include this skill (case insensitive)
        matching = []
        for j in jobs:
            for s in j.get("extracted_skills", []):
                if q == s.lower() or q in s.lower():
                    matching.append((s, j))
                    break

        if len(matching) < 2:
            return None

        # which skill matched
        skill_name = matching[0][0]
        count = len(matching)

        # which skills are often paired with this one
        co_skills = Counter()
        for _, job in matching:
            for s in job.get("extracted_skills", []):
                if s.lower() != skill_name.lower():
                    co_skills[s] += 1
        top_co = co_skills.most_common(5)

        info = f"{skill_name} appears in {count} jobs."
        if top_co:
            info += " Most frequently paired with: " + ", ".join(f"{s} ({n})" for s, n in top_co) + "."
        return info

    def _get_jobs(self) -> List[dict]:
        """Pull jobs from DB for context. Limits to recent 500."""
        if not self.db:
            return []
        try:
            return self.db.get_all_jobs(limit=500)
        except Exception as e:
            print(f"[ContextBuilder] Failed to load jobs: {e}")
            return []
