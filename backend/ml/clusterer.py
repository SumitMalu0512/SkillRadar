"""
Job Role Clustering Module.

Uses K-Means clustering on skill vectors to group similar job postings.
This helps us discover natural categories like:
  - 'Full Stack Web Development'
  - 'Data Science & ML'
  - 'DevOps & Cloud'
  - etc.
... without manually defining them.

Approach (as per project synopsis section 3.1):
  1. Build skill vectors for each job (binary or TF-IDF over skills)
  2. Find optimal K using elbow method
  3. Run K-Means
  4. Label clusters by their top frequent skills
  5. Validate with silhouette score
"""
import numpy as np
from collections import Counter
from typing import List, Dict, Tuple
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_score


class RoleClusterer:
    def __init__(self, n_clusters: int = 8, random_state: int = 42):
        self.n_clusters = n_clusters
        self.random_state = random_state
        self.vectorizer = None
        self.model = None
        self.cluster_labels = {}   # cluster_id -> human readable name
        self.cluster_top_skills = {}   # cluster_id -> [top skills]
        self.is_fitted = False

    def fit(self, jobs: List[dict]) -> Dict:
        """
        Train the clustering model on a list of jobs.

        Each job needs an 'extracted_skills' field (list of skill strings).
        Returns metrics about the clustering quality.
        """
        # filter jobs with at least one skill
        valid_jobs = [j for j in jobs if j.get("extracted_skills")]

        if len(valid_jobs) < self.n_clusters * 2:
            # not enough data to cluster well
            raise ValueError(
                f"Need at least {self.n_clusters * 2} jobs with extracted skills. "
                f"Got {len(valid_jobs)}."
            )

        # convert each job into a "document" of space-separated skills
        # we use lowercase + underscores so multi-word skills stay as one token
        docs = [
            " ".join(self._tokenize_skill(s) for s in job["extracted_skills"])
            for job in valid_jobs
        ]

        # TF-IDF vectorization
        self.vectorizer = TfidfVectorizer(
            lowercase=True,
            min_df=2,         # skill must appear in at least 2 jobs
            max_df=0.95,      # skip skills appearing in 95%+ jobs (too generic)
            token_pattern=r"(?u)\b\w[\w_]+\b",
        )
        X = self.vectorizer.fit_transform(docs)

        # K-Means clustering
        self.model = KMeans(
            n_clusters=self.n_clusters,
            random_state=self.random_state,
            n_init=10,
            max_iter=300,
        )
        clusters = self.model.fit_predict(X)

        # quality score
        try:
            sil_score = float(silhouette_score(X, clusters)) if len(set(clusters)) > 1 else 0.0
        except Exception:
            sil_score = 0.0

        # label each cluster with its top skills
        self._label_clusters(valid_jobs, clusters)

        # attach cluster id back to the original jobs
        for job, cid in zip(valid_jobs, clusters):
            job["role_cluster"] = int(cid)

        self.is_fitted = True

        return {
            "n_clusters": self.n_clusters,
            "n_jobs_clustered": len(valid_jobs),
            "silhouette_score": round(sil_score, 4),
            "cluster_labels": self.cluster_labels,
            "cluster_sizes": dict(Counter(clusters.tolist())),
        }

    def _label_clusters(self, jobs: List[dict], clusters: np.ndarray):
        """
        Generate a human readable label for each cluster based on top skills.
        e.g. cluster 0 might become 'Python · Django · PostgreSQL'
        """
        clusters_to_skills = {}
        for job, cid in zip(jobs, clusters):
            cid = int(cid)
            clusters_to_skills.setdefault(cid, []).extend(job["extracted_skills"])

        for cid, skill_list in clusters_to_skills.items():
            counter = Counter(skill_list)
            top_3 = [s for s, _ in counter.most_common(3)]
            self.cluster_top_skills[cid] = [
                {"skill": s, "count": c} for s, c in counter.most_common(10)
            ]
            self.cluster_labels[cid] = " · ".join(top_3) if top_3 else f"Cluster {cid}"

    def get_clusters_summary(self, jobs: List[dict]) -> List[Dict]:
        """
        After fitting, return a clean summary of all clusters for the UI.
        """
        if not self.is_fitted:
            raise RuntimeError("Call fit() first")

        # how many jobs in each cluster
        cluster_counts = Counter(j.get("role_cluster") for j in jobs if j.get("role_cluster") is not None)

        summary = []
        for cid in sorted(self.cluster_labels.keys()):
            summary.append({
                "cluster_id": cid,
                "label": self.cluster_labels[cid],
                "job_count": cluster_counts.get(cid, 0),
                "top_skills": self.cluster_top_skills.get(cid, [])[:8],
            })
        summary.sort(key=lambda x: x["job_count"], reverse=True)
        return summary

    def predict_cluster(self, skills: List[str]) -> int:
        """Given a list of skills, predict which cluster a job belongs to."""
        if not self.is_fitted:
            raise RuntimeError("Call fit() first")

        doc = " ".join(self._tokenize_skill(s) for s in skills)
        X = self.vectorizer.transform([doc])
        return int(self.model.predict(X)[0])

    def _tokenize_skill(self, skill: str) -> str:
        """Convert 'Machine Learning' -> 'machine_learning' so TF-IDF treats it as one token."""
        return skill.lower().replace(" ", "_").replace(".", "").replace("/", "_")

    def find_optimal_k(self, jobs: List[dict], k_range=(3, 12)) -> Dict:
        """
        Elbow method - try multiple K values and report inertia + silhouette.
        Used to justify the choice of K in the project report.
        """
        valid_jobs = [j for j in jobs if j.get("extracted_skills")]
        docs = [
            " ".join(self._tokenize_skill(s) for s in job["extracted_skills"])
            for job in valid_jobs
        ]

        vectorizer = TfidfVectorizer(
            lowercase=True, min_df=2, max_df=0.95,
            token_pattern=r"(?u)\b\w[\w_]+\b",
        )
        X = vectorizer.fit_transform(docs)

        results = []
        for k in range(k_range[0], k_range[1] + 1):
            try:
                km = KMeans(n_clusters=k, random_state=self.random_state, n_init=10)
                labels = km.fit_predict(X)
                sil = float(silhouette_score(X, labels)) if len(set(labels)) > 1 else 0
                results.append({
                    "k": k,
                    "inertia": float(km.inertia_),
                    "silhouette": round(sil, 4),
                })
            except Exception as e:
                print(f"K={k} failed: {e}")
                continue
        return {"evaluations": results}
