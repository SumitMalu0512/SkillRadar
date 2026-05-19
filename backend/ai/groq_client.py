"""
Groq LLM Client.

Wraps Groq's API for two purposes:
1. RAG-style chat where we feed job market context + user question
2. Resume tailoring suggestions for specific jobs

Uses Llama 3.1 70B by default - fast and free.
Gracefully falls back to template-based responses if no API key is set
or the API is unreachable, so the rest of the app keeps working.
"""
import os
import json
import requests
from typing import List, Dict, Optional


class GroqClient:
    BASE_URL = "https://api.groq.com/openai/v1/chat/completions"
    DEFAULT_MODEL = "llama-3.1-70b-versatile"
    FALLBACK_MODELS = [
        "llama-3.3-70b-versatile",
        "llama-3.1-8b-instant",
        "llama3-70b-8192",
    ]

    def __init__(self, api_key: Optional[str] = None, model: Optional[str] = None):
        self.api_key = api_key or os.getenv("GROQ_API_KEY", "")
        self.model = model or self.DEFAULT_MODEL
        self.is_available = bool(self.api_key)

    def chat(
        self,
        user_message: str,
        context: str = "",
        history: List[Dict] = None,
        system_prompt: Optional[str] = None,
    ) -> Dict:
        """
        Send a chat request to Groq.
        Returns {'reply': str, 'source': 'groq' | 'fallback'}
        """
        if not self.is_available:
            return {
                "reply": self._fallback_chat(user_message, context),
                "source": "fallback",
            }

        sys = system_prompt or self._default_system_prompt()
        messages = [{"role": "system", "content": sys}]

        if context:
            messages.append({
                "role": "system",
                "content": f"Here is relevant data from the SkillRadar job market database:\n\n{context}",
            })

        for h in (history or []):
            if h.get("role") in ("user", "assistant") and h.get("content"):
                messages.append({"role": h["role"], "content": h["content"]})

        messages.append({"role": "user", "content": user_message})

        # try models in order until one works
        models_to_try = [self.model] + [m for m in self.FALLBACK_MODELS if m != self.model]
        last_error = None
        for model in models_to_try:
            try:
                resp = requests.post(
                    self.BASE_URL,
                    headers={
                        "Authorization": f"Bearer {self.api_key}",
                        "Content-Type": "application/json",
                    },
                    json={
                        "model": model,
                        "messages": messages,
                        "temperature": 0.7,
                        "max_tokens": 800,
                    },
                    timeout=25,
                )
                if resp.status_code == 200:
                    data = resp.json()
                    reply = data["choices"][0]["message"]["content"].strip()
                    return {"reply": reply, "source": "groq", "model_used": model}
                else:
                    last_error = f"{resp.status_code}: {resp.text[:200]}"
                    # if it's an auth error, no point trying other models
                    if resp.status_code == 401:
                        break
            except requests.RequestException as e:
                last_error = str(e)
                continue

        print(f"[Groq] All models failed. Last error: {last_error}")
        return {
            "reply": self._fallback_chat(user_message, context),
            "source": "fallback",
            "error": last_error,
        }

    def resume_suggestions(
        self,
        resume_text: str,
        job_title: str,
        job_description: str,
        missing_skills: List[str],
        matched_skills: List[str],
        match_score: float,
    ) -> Dict:
        """
        Generate resume tailoring suggestions for a specific job.
        """
        prompt = f"""I want to apply for this job: "{job_title}".

My current match score for this job is {match_score}%.

Skills I have that match this job: {', '.join(matched_skills[:15]) or 'none yet'}
Skills the job requires that I am missing: {', '.join(missing_skills[:15]) or 'none'}

Job description excerpt:
{job_description[:1200]}

My resume excerpt:
{resume_text[:1500]}

Please give me 4-6 SPECIFIC, ACTIONABLE suggestions to improve my resume for this exact job. Be concrete and practical. For each suggestion:
1. Start with a clear action verb
2. Mention the specific keywords or phrases to add
3. Suggest WHERE in the resume to add it

Format the response as a numbered list. Be concise. Do not include any disclaimers or generic advice."""

        result = self.chat(
            user_message=prompt,
            system_prompt="You are an expert technical recruiter who helps candidates tailor resumes for specific jobs. You give practical, specific advice based on the job description and the candidate's actual resume.",
        )
        return result

    def _default_system_prompt(self) -> str:
        return (
            "You are SkillRadar Assistant, a friendly AI helper for job seekers and students "
            "exploring the job market. You have access to live job market data including "
            "skills, trends, role clusters, and forecasts. "
            "Answer questions accurately based on the provided context data. "
            "Be conversational, concise (max 3-4 paragraphs), and practical. "
            "When asked about specific skills or trends, refer to the actual numbers from the context. "
            "If the context doesn't have the answer, say so honestly rather than making things up. "
            "Format responses with markdown for readability when helpful."
        )

    def _fallback_chat(self, user_message: str, context: str) -> str:
        """
        Rule-based fallback when Groq is unavailable.
        Gives a useful response even without the LLM.
        """
        msg = user_message.lower()

        if not self.is_available:
            return (
                "The AI chat feature requires a Groq API key to provide intelligent responses. "
                "However, you can still explore the job market data through the dashboard pages: "
                "**Jobs** for live search, **Skills** for trending analytics, **Roles** for "
                "clustered career paths, and **Forecast** for future skill demand predictions."
            )

        # Pattern-based responses using the context we DO have
        if any(w in msg for w in ["trending", "popular", "in demand", "hot skills"]):
            return f"Based on current job market data:\n\n{context[:600]}\n\nCheck the Skills Analytics page for more details and visualizations."
        if any(w in msg for w in ["forecast", "future", "predict", "next year"]):
            return "Take a look at the Forecast page where we show 90-day skill demand predictions based on time-series analysis of job posting patterns."
        if any(w in msg for w in ["cluster", "role", "career path"]):
            return f"Job roles cluster into natural groupings. Here's what we found:\n\n{context[:500]}\n\nVisit the Roles page to explore each cluster interactively."

        return (
            "I can help you understand the job market based on real data from SkillRadar. "
            "Try asking about: trending skills, role clusters, salary ranges, or which "
            "skills are growing fastest. You can also explore the analytics pages directly."
        )
