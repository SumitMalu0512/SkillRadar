"""
Resume Parser & Analyzer.

Extracts text from a PDF resume and runs it through our existing NLP
skill extractor. Also infers experience level and target role from the text.
"""
import re
import io
from typing import Optional, Dict, List
from collections import Counter

try:
    from pypdf import PdfReader
    PDF_LIB = "pypdf"
except ImportError:
    try:
        from PyPDF2 import PdfReader
        PDF_LIB = "PyPDF2"
    except ImportError:
        PdfReader = None
        PDF_LIB = None


class ResumeParser:
    def __init__(self, skill_extractor):
        self.extractor = skill_extractor

    def parse_pdf(self, pdf_bytes: bytes) -> Dict:
        """
        Parse a PDF resume from raw bytes.
        Returns dict with text + analysis.
        """
        if PdfReader is None:
            return {
                "error": "PDF library not installed. Run: pip install pypdf",
                "text": "",
                "skills": [],
            }

        try:
            reader = PdfReader(io.BytesIO(pdf_bytes))
            text_parts = []
            for page in reader.pages:
                try:
                    text_parts.append(page.extract_text() or "")
                except Exception:
                    continue
            full_text = "\n".join(text_parts)
        except Exception as e:
            return {
                "error": f"Could not read PDF: {str(e)}",
                "text": "",
                "skills": [],
            }

        if not full_text.strip():
            return {
                "error": "Could not extract text from PDF. It might be image-based (scanned). Try a text-based PDF.",
                "text": "",
                "skills": [],
            }

        return self.analyze(full_text)

    def analyze(self, text: str) -> Dict:
        """
        Run full analysis on a resume text.
        Returns skills, experience level, target roles, and summary.
        """
        clean = self._clean_text(text)

        # extract skills using our existing engine
        skill_details = self.extractor.extract_with_details(clean)
        skills = [d["skill"] for d in skill_details]

        # infer experience level from common phrases
        experience_years = self._estimate_experience_years(clean)
        experience_level = self._classify_experience(experience_years)

        # infer target roles from titles mentioned
        target_roles = self._extract_target_roles(clean)

        # candidate name / first non-empty line is often the name
        name = self._extract_name(text)

        # email / phone
        email = self._extract_email(text)

        return {
            "text": clean,
            "name": name,
            "email": email,
            "skills": skills,
            "skill_details": skill_details,
            "experience_years": experience_years,
            "experience_level": experience_level,
            "target_roles": target_roles,
            "word_count": len(clean.split()),
            "error": None,
        }

    def _clean_text(self, text: str) -> str:
        # collapse multiple whitespace into single space (but keep newlines)
        lines = text.split("\n")
        cleaned = [re.sub(r"\s+", " ", line).strip() for line in lines]
        return "\n".join(line for line in cleaned if line)

    def _estimate_experience_years(self, text: str) -> Optional[float]:
        """
        Look for patterns like 'X years of experience', 'X+ years'.
        Returns the highest number found.
        """
        patterns = [
            r"(\d+(?:\.\d+)?)\s*\+?\s*years?\s+of\s+(?:experience|work)",
            r"(\d+(?:\.\d+)?)\s*\+?\s*yrs?\s+(?:of\s+)?(?:experience|exp)",
            r"experience\s*[:\-]?\s*(\d+(?:\.\d+)?)\s*\+?\s*years?",
        ]
        years_found = []
        for pat in patterns:
            for match in re.finditer(pat, text, re.IGNORECASE):
                try:
                    years_found.append(float(match.group(1)))
                except (ValueError, IndexError):
                    pass
        return max(years_found) if years_found else None

    def _classify_experience(self, years: Optional[float]) -> str:
        if years is None:
            return "unspecified"
        if years < 1:
            return "fresher"
        elif years < 3:
            return "junior"
        elif years < 6:
            return "mid-level"
        elif years < 10:
            return "senior"
        else:
            return "lead"

    def _extract_target_roles(self, text: str) -> List[str]:
        """
        Look for common job title phrases in the resume.
        Returns the most likely target roles.
        """
        # common role patterns - case insensitive whole phrase matching
        role_patterns = [
            "Software Engineer", "Software Developer", "Senior Software Engineer",
            "Full Stack Developer", "Full Stack Engineer", "Frontend Developer",
            "Backend Developer", "Web Developer", "Python Developer",
            "Java Developer", "React Developer", "Node.js Developer",
            "Angular Developer", "Mobile Developer", "Android Developer",
            "iOS Developer", "React Native Developer", "Flutter Developer",
            "Data Scientist", "Data Analyst", "Data Engineer", "Analytics Engineer",
            "Machine Learning Engineer", "ML Engineer", "AI Engineer",
            "DevOps Engineer", "Cloud Engineer", "Site Reliability Engineer",
            "QA Engineer", "Test Engineer", "Security Engineer",
            "Database Administrator", "Solutions Architect", "Technical Architect",
            "Product Manager", "Project Manager", "Business Analyst",
            "UI UX Designer", "Engineering Manager", "Tech Lead", "Team Lead",
        ]

        found = Counter()
        text_lower = text.lower()
        for role in role_patterns:
            # match whole phrase
            count = text_lower.count(role.lower())
            if count > 0:
                found[role] = count

        # top 3 by frequency
        return [role for role, _ in found.most_common(3)]

    def _extract_name(self, text: str) -> str:
        """
        Take the first non-empty line that looks like a name.
        Heuristic: 2-4 words, mostly letters, no special chars except spaces/dots.
        """
        for line in text.split("\n")[:5]:
            line = line.strip()
            if not line or len(line) > 60 or len(line) < 4:
                continue
            words = line.split()
            if 1 < len(words) <= 4 and all(re.match(r"^[A-Za-z][A-Za-z.\-']*$", w) for w in words):
                return line
        return ""

    def _extract_email(self, text: str) -> str:
        match = re.search(r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}", text)
        return match.group(0) if match else ""
