import os
import requests
import time
from flask import current_app

# -----------------------------------------------
# 🔑 Configuration
# -----------------------------------------------
RAPIDAPI_KEY = os.getenv("RAPIDAPI_KEY")
RAPIDAPI_HOST = "jsearch.p.rapidapi.com"

# -----------------------------------------------
# ⚙️ Global caches
# -----------------------------------------------
_cache = {"timestamp": 0, "query": "", "data": []}  # List search cache (for /jobs)
_job_cache = {}  # Per-job detail cache (for /jobs/<id>)

# -----------------------------------------------
# 🔍 Fetch jobs from RapidAPI (JSearch)
# -----------------------------------------------
def fetch_jobs_from_rapidapi(title=None, location=None, limit=20):
    """
    Fetch job listings using the JSearch (RapidAPI) endpoint.
    Includes caching for both list results and per-job details.
    """
    global _cache, _job_cache

    query = f"{title or 'developer'} in {location or 'India'}"

    # ✅ Return cached results if recent (within 60s) and same query
    if time.time() - _cache["timestamp"] < 60 and _cache["query"] == query:
        current_app.logger.info(f"♻️ Using cached RapidAPI results for '{query}'")
        return _cache["data"]

    url = f"https://{RAPIDAPI_HOST}/search"
    headers = {
        "x-rapidapi-key": RAPIDAPI_KEY,
        "x-rapidapi-host": RAPIDAPI_HOST,
    }
    params = {"query": query, "num_pages": 1}

    try:
        response = requests.get(url, headers=headers, params=params, timeout=5)
        response.raise_for_status()
        data = response.json().get("data", [])

        jobs = []
        for job in data[:limit]:
            job_obj = {
                "id": job.get("job_id", ""),
                "title": job.get("job_title", "Untitled"),
                "company": job.get("employer_name", "Unknown"),
                "location": job.get("job_city") or job.get("job_country") or "India",
                "job_type": job.get("job_employment_type", "Full-time"),
                "salary": (
                    job.get("job_min_salary")
                    and f"₹{job.get('job_min_salary')}+"
                )
                or "₹ Not Specified",
                "description": (job.get("job_description") or "No description available")[:400],
                "url": job.get("job_apply_link", "#"),
                "posted_date": job.get("job_posted_at_datetime_utc", "Recently"),
                "remote": bool(job.get("job_is_remote", False)),
                "source": "RapidAPI (JSearch)",
            }

            jobs.append(job_obj)

            # ✅ Store job in detail cache
            if job_obj["id"]:
                _job_cache[job_obj["id"]] = job_obj

        # ✅ Update list cache
        _cache = {"timestamp": time.time(), "query": query, "data": jobs}
        current_app.logger.info(f"✅ RapidAPI returned {len(jobs)} jobs for query '{query}'")

        return jobs

    except Exception as e:
        current_app.logger.warning(f"⚠️ RapidAPI fetch failed: {e}")
        return []


# -----------------------------------------------
# 🔎 Get job by ID from cache
# -----------------------------------------------
def get_job_by_id_from_cache(job_id):
    """
    Retrieve a single job by ID from RapidAPI cache (either _job_cache or _cache["data"]).
    Ensures job detail pages work even after refresh.
    """
    global _cache, _job_cache

    if not job_id:
        return None

    # 1️⃣ Try per-job detail cache
    if job_id in _job_cache:
        current_app.logger.info(f"♻️ Found job {job_id} in detailed RapidAPI cache")
        return _job_cache[job_id]

    # 2️⃣ Try list cache
    if _cache.get("data"):
        match = next((j for j in _cache["data"] if str(j.get("id")) == str(job_id)), None)
        if match:
            _job_cache[job_id] = match  # store for next time
            current_app.logger.info(f"♻️ Found job {job_id} in list cache")
            return match

    # 3️⃣ Not found
    current_app.logger.warning(f"⚠️ Job {job_id} not found in RapidAPI cache")
    return None


# -----------------------------------------------
# 🧹 Optional utility: clear caches (for testing)
# -----------------------------------------------
def clear_rapidapi_cache():
    """Manually clear RapidAPI caches (useful for debugging)."""
    global _cache, _job_cache
    _cache = {"timestamp": 0, "query": "", "data": []}
    _job_cache = {}
    current_app.logger.info("🧹 Cleared all RapidAPI caches.")
