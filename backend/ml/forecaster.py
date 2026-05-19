"""
Skill Demand Forecasting Module.

Uses Facebook Prophet to predict future demand for skills based on
historical job posting data. When Prophet is unavailable or fails at
runtime (common on Windows due to its C++ backend), we fall back to a
linear regression model with weekly seasonality. The fallback produces
visually similar forecasts and is more reliable across platforms.

When jobs are ingested in a single batch (typical for demos), there's no
real day by day history. The forecaster augments sparse data with a
realistic baseline derived from observed frequencies plus weekly
seasonality patterns. The is_synthetic flag indicates when augmentation
was applied.
"""
import pandas as pd
import numpy as np
import random
from datetime import datetime, timedelta
from collections import defaultdict, Counter
from typing import List, Dict, Optional


class SkillForecaster:
    def __init__(self):
        # we set this to False so we don't even try Prophet
        # the linear forecaster works great and is rock-solid on Windows
        self._prophet_available = self._try_init_prophet()

    def _try_init_prophet(self) -> bool:
        """
        Try to actually instantiate a Prophet model. Just checking the import
        isn't enough - on Windows, Prophet often imports fine but crashes
        when you try to use it (stan_backend issue).
        """
        try:
            from prophet import Prophet
            # try to make a tiny test model to verify it actually works
            test = Prophet()
            df = pd.DataFrame({
                "ds": pd.date_range("2024-01-01", periods=10),
                "y": list(range(10))
            })
            test.fit(df)
            print("[Forecaster] Prophet initialized successfully")
            return True
        except Exception as e:
            print(f"[Forecaster] Prophet unavailable ({type(e).__name__}) - using linear model with weekly seasonality")
            return False

    def forecast_skill(
        self,
        jobs: List[dict],
        skill: str,
        forecast_days: int = 90,
    ) -> Optional[Dict]:
        history = self._build_skill_timeseries(jobs, skill)
        is_synthetic = False

        if len(history) < 14:
            history = self._augment_history(jobs, skill, history)
            is_synthetic = True

        if len(history) < 5:
            return None

        # try Prophet first; if it errors at runtime, fall back to linear
        forecast = None
        if self._prophet_available:
            try:
                forecast = self._prophet_forecast(history, forecast_days)
            except Exception as e:
                # Prophet failed at predict time - flag it and never try again
                print(f"[Forecaster] Prophet failed for {skill}: {e}. Falling back permanently.")
                self._prophet_available = False

        if forecast is None:
            forecast = self._linear_forecast(history, forecast_days)

        trend = self._classify_trend(history, forecast)

        return {
            "skill": skill,
            "history": history,
            "forecast": forecast,
            "trend": trend,
            "is_synthetic": is_synthetic,
        }

    def forecast_top_skills(
        self,
        jobs: List[dict],
        top_n: int = 10,
        forecast_days: int = 90,
    ) -> List[Dict]:
        counter = Counter()
        for job in jobs:
            for s in set(job.get("extracted_skills", [])):
                counter[s] += 1

        top_skills = [s for s, _ in counter.most_common(top_n)]
        results = []
        for s in top_skills:
            try:
                f = self.forecast_skill(jobs, s, forecast_days)
                if f:
                    results.append(f)
            except Exception as e:
                print(f"[Forecaster] Skipping {s}: {e}")
                continue
        return results

    def _build_skill_timeseries(self, jobs: List[dict], skill: str) -> List[Dict]:
        daily_counts = defaultdict(int)
        for job in jobs:
            date_str = job.get("posted_date") or job.get("fetched_at")
            if not date_str or skill not in job.get("extracted_skills", []):
                continue
            try:
                day = str(date_str)[:10]
                datetime.strptime(day, "%Y-%m-%d")
                daily_counts[day] += 1
            except (ValueError, TypeError):
                continue
        return [
            {"date": d, "demand": daily_counts[d]}
            for d in sorted(daily_counts.keys())
        ]

    def _augment_history(self, jobs: List[dict], skill: str, real_history: List[Dict]) -> List[Dict]:
        """
        Generate realistic 60-day baseline based on observed frequency
        plus weekly seasonality (Tue-Wed peaks, weekend dips).
        """
        skill_count = sum(1 for j in jobs if skill in j.get("extracted_skills", []))
        if skill_count == 0:
            return real_history

        total_jobs = len(jobs)
        base_daily = max(1.0, (skill_count / max(total_jobs, 1)) * 8)

        synthetic = []
        end_date = datetime.now() - timedelta(days=1)
        random.seed(hash(skill) % (2**31))

        weekday_factors = {
            0: 1.05, 1: 1.15, 2: 1.20, 3: 1.10,
            4: 0.95, 5: 0.55, 6: 0.50,
        }

        for i in range(60, 0, -1):
            day = end_date - timedelta(days=i)
            weekday = day.weekday()
            factor = weekday_factors.get(weekday, 1.0)
            trend = 1.0 + (60 - i) * 0.003
            noise = random.uniform(0.75, 1.25)
            demand = max(0, round(base_daily * factor * trend * noise))
            synthetic.append({
                "date": day.strftime("%Y-%m-%d"),
                "demand": demand,
            })

        real_dates = {h["date"] for h in real_history}
        merged = [s for s in synthetic if s["date"] not in real_dates] + real_history
        merged.sort(key=lambda x: x["date"])
        return merged

    def _prophet_forecast(self, history: List[Dict], days: int) -> List[Dict]:
        from prophet import Prophet
        import logging
        logging.getLogger("prophet").setLevel(logging.WARNING)
        logging.getLogger("cmdstanpy").setLevel(logging.WARNING)

        df = pd.DataFrame(history)
        df.columns = ["ds", "y"]
        df["ds"] = pd.to_datetime(df["ds"])

        model = Prophet(
            daily_seasonality=False,
            weekly_seasonality=True,
            yearly_seasonality=False,
            interval_width=0.80,
        )
        model.fit(df)

        future = model.make_future_dataframe(periods=days)
        forecast = model.predict(future)

        last_history_date = df["ds"].max()
        future_only = forecast[forecast["ds"] > last_history_date]

        return [
            {
                "date": row["ds"].strftime("%Y-%m-%d"),
                "predicted": max(0, round(row["yhat"], 2)),
                "lower": max(0, round(row["yhat_lower"], 2)),
                "upper": max(0, round(row["yhat_upper"], 2)),
            }
            for _, row in future_only.iterrows()
        ]

    def _linear_forecast(self, history: List[Dict], days: int) -> List[Dict]:
        """
        Linear regression with weekly seasonality and trend.
        Reliable cross-platform, produces results visually similar to Prophet.
        """
        x = np.arange(len(history))
        y = np.array([h["demand"] for h in history], dtype=float)

        # fit a linear trend
        if len(history) >= 2:
            coeffs = np.polyfit(x, y, 1)
            slope, intercept = float(coeffs[0]), float(coeffs[1])
        else:
            slope, intercept = 0.0, float(y[0]) if len(y) else 1.0

        last_date = datetime.strptime(history[-1]["date"], "%Y-%m-%d")
        std_dev = float(y.std()) if len(y) > 1 else 1.0

        weekday_factors = [1.05, 1.15, 1.20, 1.10, 0.95, 0.55, 0.50]

        forecast = []
        for i in range(1, days + 1):
            future_x = len(history) + i - 1
            base_pred = max(0, slope * future_x + intercept)
            future_date = last_date + timedelta(days=i)
            factor = weekday_factors[future_date.weekday()]
            pred = base_pred * factor

            # confidence band widens slightly into the future
            uncertainty = std_dev * (1 + i * 0.005)

            forecast.append({
                "date": future_date.strftime("%Y-%m-%d"),
                "predicted": round(pred, 2),
                "lower": round(max(0, pred - uncertainty), 2),
                "upper": round(pred + uncertainty, 2),
            })
        return forecast

    def _classify_trend(self, history: List[Dict], forecast: List[Dict]) -> str:
        if not history or not forecast:
            return "stable"
        recent_avg = sum(h["demand"] for h in history[-7:]) / max(1, len(history[-7:]))
        future_avg = sum(f["predicted"] for f in forecast[:30]) / max(1, len(forecast[:30]))
        if future_avg > recent_avg * 1.15:
            return "rising"
        elif future_avg < recent_avg * 0.85:
            return "falling"
        else:
            return "stable"
