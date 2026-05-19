"""
Unified job posting model.

Each job API returns data in its own weird format. We normalize
everything into this single structure so the rest of the app
doesn't need to know which API a job came from.
"""
from dataclasses import dataclass, asdict, field
from typing import Optional, List
from datetime import datetime


@dataclass
class JobPosting:
    # core identifying fields
    job_id: str                          # unique ID we generate
    source: str                          # 'adzuna' / 'remotive' / 'jsearch'
    source_url: str                      # original posting URL

    # what the user sees
    title: str
    company: str
    location: str
    description: str

    # optional but useful
    salary_min: Optional[float] = None
    salary_max: Optional[float] = None
    salary_currency: Optional[str] = None
    employment_type: Optional[str] = None    # full-time, contract, etc
    is_remote: bool = False
    posted_date: Optional[str] = None        # ISO format

    # filled in later by NLP pipeline
    extracted_skills: List[str] = field(default_factory=list)
    role_cluster: Optional[int] = None

    # internal tracking
    fetched_at: str = field(default_factory=lambda: datetime.now().isoformat())

    def to_dict(self):
        return asdict(self)

    @property
    def has_salary(self):
        return self.salary_min is not None or self.salary_max is not None

    @property
    def salary_display(self):
        if not self.has_salary:
            return "Not disclosed"
        cur = self.salary_currency or ""
        if self.salary_min and self.salary_max:
            return f"{cur} {self.salary_min:,.0f} - {self.salary_max:,.0f}"
        elif self.salary_min:
            return f"{cur} {self.salary_min:,.0f}+"
        else:
            return f"Up to {cur} {self.salary_max:,.0f}"
