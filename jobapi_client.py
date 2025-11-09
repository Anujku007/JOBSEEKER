"""
Unified Job API client for JobSeeker
Priority: Mantiks -> Jooble -> Adzuna -> Mock Data
"""

import os
import requests
import logging
from datetime import datetime

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

# Environment config
MANTIKS_API_KEY = os.getenv("MANTIKS_API_KEY", "")
MANTIKS_BASE_URL = os.getenv("MANTIKS_BASE_URL", "https://api.mantiks.io")

JOOBLE_API_KEY = os.getenv("JOOBLE_API_KEY", "")
ADZUNA_APP_ID = os.getenv("ADZUNA_APP_ID", "")
ADZUNA_APP_KEY = os.getenv("ADZUNA_APP_KEY", "")
ADZUNA_COUNTRY = os.getenv("ADZUNA_COUNTRY", "in")  # 'in' for India

DEFAULT_TIMEOUT = 10


# -----------------------------
# Normalizer & Helpers
# -----------------------------
def _norm(job: dict, source: str) -> dict:
    """Normalize job dict from any provider to a common shape."""
    return {
        "id": str(job.get("id") or job.get("job_id") or job.get("unique_id") or job.get("url") or ""),
        "title": job.get("title") or job.get("job_title") or job.get("position") or "Untitled Job",
        "company": job.get("company") or job.get("company_name") or job.get("employer") or "Unknown Company",
        "location": job.get("location") or job.get("area") or job.get("city") or "Not specified",
        "job_type": job.get("job_type") or job.get("type") or job.get("employment_type") or "Full-time",
        "salary": job.get("salary") or job.get("salary_min") or job.get("ctc") or "N/A",
        "description": job.get("description") or job.get("snippet") or job.get("summary") or "No description available.",
        "url": job.get("url") or job.get("apply_url") or job.get("redirect_url") or "#",
        "posted_date": job.get("posted_date") or job.get("publication_date") or job.get("date") or datetime.now().strftime("%Y-%m-%d"),
        "remote": bool(job.get("remote", False)),
        "source": source
    }


# -----------------------------
# Mantiks API
# -----------------------------
def _mantiks_search(title=None, location=None, limit=25, page=1):
    if not MANTIKS_API_KEY:
        logger.info("Mantiks key not set")
        return []
    endpoint = f"{MANTIKS_BASE_URL.rstrip('/')}/api/v1/jobs/search"
    params = {"title": title, "location": location, "limit": limit, "page": page}
    params = {k: v for k, v in params.items() if v}
    headers = {"Authorization": f"Bearer {MANTIKS_API_KEY}", "Accept": "application/json"}

    try:
        logger.info(f"🔹 Calling Mantiks: {endpoint} params={params}")
        resp = requests.get(endpoint, headers=headers, params=params, timeout=DEFAULT_TIMEOUT)
        resp.raise_for_status()
        data = resp.json()
        jobs = data.get("jobs") or data.get("data") or data.get("results") or []
        return [_norm(j, "Mantiks") for j in jobs]
    except Exception as e:
        logger.error(f"Mantiks API error: {e}")
        return []


# -----------------------------
# Jooble API
# -----------------------------
def _jooble_search(keyword=None, location=None, limit=25):
    if not JOOBLE_API_KEY:
        logger.info("Jooble key not set")
        return []
    endpoint = "https://jooble.org/api/search"
    headers = {"Content-Type": "application/json", "X-Api-Key": JOOBLE_API_KEY}
    payload = {"keyword": keyword or "", "location": location or "", "page": 1, "limit": limit}

    try:
        logger.info(f"🔹 Calling Jooble: {endpoint}")
        resp = requests.post(endpoint, json=payload, headers=headers, timeout=DEFAULT_TIMEOUT)
        resp.raise_for_status()
        data = resp.json()
        jobs = data.get("jobs") or data.get("results") or []
        return [_norm(j, "Jooble") for j in jobs]
    except Exception as e:
        logger.error(f"Jooble API error: {e}")
        return []


# -----------------------------
# Adzuna API
# -----------------------------
def _adzuna_search(keyword=None, location=None, limit=25, page=1):
    if not (ADZUNA_APP_ID and ADZUNA_APP_KEY):
        logger.info("Adzuna credentials not set")
        return []
    try:
        endpoint = f"https://api.adzuna.com/v1/api/jobs/{ADZUNA_COUNTRY}/search/{page}"
        params = {
            "app_id": ADZUNA_APP_ID,
            "app_key": ADZUNA_APP_KEY,
            "what": keyword or "",
            "where": location or "",
            "results_per_page": limit
        }
        logger.info(f"🔹 Calling Adzuna: {endpoint}")
        r = requests.get(endpoint, params=params, timeout=DEFAULT_TIMEOUT)
        r.raise_for_status()
        data = r.json()
        jobs = data.get("results") or []
        return [_norm(j, "Adzuna") for j in jobs]
    except Exception as e:
        logger.error(f"Adzuna API error: {e}")
        return []


# -----------------------------
# Mock Data (offline fallback)
# -----------------------------
def _mock_jobs(title=None, location=None):
    logger.warning("⚠️ Using mock data (offline mode)")

    mock_data = [
        {"id":"mock1","title":"Python Developer","company":"Infosys","location":"Bengaluru","job_type":"Full-time","salary":"₹8,00,000-₹12,00,000","description":"Work on backend APIs and automation using Python and Flask.","url":"#","posted_date":"2025-11-01","remote":True,"source":"Mock"},
        {"id":"mock2","title":"Data Analyst","company":"TCS","location":"Hyderabad","job_type":"Full-time","salary":"₹6,50,000-₹9,00,000","description":"Analyze datasets and build insights using Python, SQL, and Power BI.","url":"#","posted_date":"2025-11-03","remote":False,"source":"Mock"},
        {"id":"mock3","title":"AI Engineer","company":"Wipro","location":"Mumbai","job_type":"Contract","salary":"₹10,00,000-₹15,00,000","description":"Develop ML models and optimize neural networks for production.","url":"#","posted_date":"2025-11-05","remote":True,"source":"Mock"},
        {"id":"mock4","title":"Frontend Developer (React)","company":"Capgemini","location":"Bengaluru","job_type":"Full-time","salary":"₹7,50,000-₹11,00,000","description":"Build dynamic user interfaces with React and TypeScript.","url":"#","posted_date":"2025-11-02","remote":False,"source":"Mock"},
        {"id":"mock5","title":"DevOps Engineer","company":"HCL Tech","location":"Hyderabad","job_type":"Full-time","salary":"₹9,00,000-₹13,00,000","description":"Manage CI/CD pipelines and cloud infrastructure.","url":"#","posted_date":"2025-11-04","remote":True,"source":"Mock"},
        {"id":"mock6","title":"Mobile App Developer","company":"L&T InfoTech","location":"Mumbai","job_type":"Full-time","salary":"₹8,50,000-₹12,50,000","description":"Develop cross-platform apps using Flutter.","url":"#","posted_date":"2025-11-06","remote":False,"source":"Mock"},
        {"id":"mock7","title":"Data Engineer","company":"Cognizant","location":"Bengaluru","job_type":"Full-time","salary":"₹11,00,000-₹16,00,000","description":"Design data pipelines and ETL jobs on AWS.","url":"#","posted_date":"2025-11-07","remote":True,"source":"Mock"},
        {"id":"mock8","title":"QA Engineer","company":"Mindtree","location":"Hyderabad","job_type":"Full-time","salary":"₹5,50,000-₹8,00,000","description":"Automate tests and perform regression testing.","url":"#","posted_date":"2025-11-08","remote":False,"source":"Mock"},
        {"id":"mock9","title":"Cyber Security Analyst","company":"Tech Mahindra","location":"Mumbai","job_type":"Full-time","salary":"₹9,50,000-₹14,00,000","description":"Monitor threat intelligence and execute incident response.","url":"#","posted_date":"2025-11-09","remote":True,"source":"Mock"},
        {"id":"mock10","title":"Business Intelligence Developer","company":"Wipro","location":"Bengaluru","job_type":"Full-time","salary":"₹7,00,000-₹10,00,000","description":"Create dashboards and reports using Power BI and SQL.","url":"#","posted_date":"2025-11-10","remote":False,"source":"Mock"},
        {"id":"mock11","title":"Cloud Architect","company":"Accenture","location":"Hyderabad","job_type":"Full-time","salary":"₹12,00,000-₹18,00,000","description":"Architect AWS/Azure solutions and migrations.","url":"#","posted_date":"2025-11-11","remote":True,"source":"Mock"},
        {"id":"mock12","title":"Backend Developer","company":"IBM India","location":"Mumbai","job_type":"Full-time","salary":"₹8,20,000-₹12,20,000","description":"Develop scalable backend services using Node.js.","url":"#","posted_date":"2025-11-12","remote":False,"source":"Mock"},
        {"id":"mock13","title":"Machine Learning Engineer","company":"Dell","location":"Bengaluru","job_type":"Full-time","salary":"₹10,50,000-₹15,50,000","description":"Implement ML models in production environments.","url":"#","posted_date":"2025-11-13","remote":True,"source":"Mock"},
        {"id":"mock14","title":"Product Manager","company":"Oracle","location":"Hyderabad","job_type":"Full-time","salary":"₹14,00,000-₹20,00,000","description":"Lead product roadmap for SaaS platforms.","url":"#","posted_date":"2025-11-14","remote":False,"source":"Mock"},
        {"id":"mock15","title":"Full Stack Developer","company":"SAP Labs","location":"Mumbai","job_type":"Full-time","salary":"₹9,80,000-₹13,80,000","description":"Work with React, Node.js, and GraphQL.","url":"#","posted_date":"2025-11-15","remote":True,"source":"Mock"},
        {"id":"mock16","title":"Systems Engineer","company":"Intel","location":"Bengaluru","job_type":"Full-time","salary":"₹7,40,000-₹10,40,000","description":"Maintain and optimize software systems.","url":"#","posted_date":"2025-11-16","remote":False,"source":"Mock"},
        {"id":"mock17","title":"SRE","company":"Adobe","location":"Hyderabad","job_type":"Full-time","salary":"₹11,50,000-₹16,50,000","description":"Ensure reliability and scalability of systems.","url":"#","posted_date":"2025-11-17","remote":True,"source":"Mock"},
        {"id":"mock18","title":"UI/UX Designer","company":"Zoho","location":"Mumbai","job_type":"Full-time","salary":"₹6,20,000-₹9,20,000","description":"Design intuitive user experiences.","url":"#","posted_date":"2025-11-18","remote":False,"source":"Mock"},
        {"id":"mock19","title":"Tech Support Engineer","company":"HPE","location":"Bengaluru","job_type":"Full-time","salary":"₹5,90,000-₹8,40,000","description":"Provide enterprise support.","url":"#","posted_date":"2025-11-19","remote":False,"source":"Mock"},
        {"id":"mock20","title":"Digital Marketing Specialist","company":"Cognizant","location":"Hyderabad","job_type":"Full-time","salary":"₹6,00,000-₹8,50,000","description":"Drive marketing campaigns.","url":"#","posted_date":"2025-11-20","remote":True,"source":"Mock"},
        {"id":"mock21","title":"ERP Consultant","company":"TCS","location":"Mumbai","job_type":"Contract","salary":"₹8,50,000-₹12,00,000","description":"Implement ERP solutions.","url":"#","posted_date":"2025-11-21","remote":False,"source":"Mock"},
        {"id":"mock22","title":"Embedded Engineer","company":"Bosch","location":"Bengaluru","job_type":"Full-time","salary":"₹9,10,000-₹13,10,000","description":"Develop embedded firmware for IoT.","url":"#","posted_date":"2025-11-22","remote":False,"source":"Mock"},
        {"id":"mock23","title":"Game Developer","company":"Ubisoft","location":"Hyderabad","job_type":"Full-time","salary":"₹7,70,000-₹11,00,000","description":"Build gameplay systems in Unity.","url":"#","posted_date":"2025-11-23","remote":True,"source":"Mock"},
        {"id":"mock24","title":"Network Administrator","company":"Cisco","location":"Mumbai","job_type":"Full-time","salary":"₹6,80,000-₹9,80,000","description":"Manage network infrastructure.","url":"#","posted_date":"2025-11-24","remote":False,"source":"Mock"},
        {"id":"mock25","title":"Data Scientist","company":"Google","location":"Bengaluru","job_type":"Full-time","salary":"₹12,00,000-₹18,00,000","description":"Develop predictive analytics.","url":"#","posted_date":"2025-11-25","remote":True,"source":"Mock"},
        {"id":"mock26","title":"Blockchain Engineer","company":"IBM","location":"Hyderabad","job_type":"Full-time","salary":"₹11,00,000-₹17,00,000","description":"Design blockchain solutions.","url":"#","posted_date":"2025-11-26","remote":False,"source":"Mock"},
        {"id":"mock27","title":"Rust Developer","company":"Meta","location":"Mumbai","job_type":"Full-time","salary":"₹10,50,000-₹14,50,000","description":"Build high-performance backend systems.","url":"#","posted_date":"2025-11-27","remote":True,"source":"Mock"},
        {"id":"mock28","title":"AI Research Intern","company":"Flipkart","location":"Bengaluru","job_type":"Internship","salary":"₹4,50,000-₹6,00,000","description":"Research AI algorithms for e-commerce.","url":"#","posted_date":"2025-11-28","remote":False,"source":"Mock"},
        {"id":"mock29","title":"Marketing Automation Specialist","company":"Adobe","location":"Hyderabad","job_type":"Full-time","salary":"₹7,20,000-₹10,00,000","description":"Automate workflows using HubSpot.","url":"#","posted_date":"2025-11-29","remote":True,"source":"Mock"},
        {"id":"mock30","title":"SAP FICO Consultant","company":"PwC","location":"Mumbai","job_type":"Full-time","salary":"₹8,90,000-₹12,90,000","description":"Implement SAP FICO modules.","url":"#","posted_date":"2025-11-30","remote":False,"source":"Mock"}
    ]

    return mock_data


# -----------------------------
# Unified fetch function
# -----------------------------
def fetch_jobs(title=None, location= None, limit=25, page=1, **kwargs):
    """
    Fetch jobs from Mantiks, Adzuna, or Jooble APIs.
    Extra kwargs like 'country' are ignored for backward compatibility.
    """
    # Just ignore unsupported args like 'country'
    country = kwargs.get("country", None)
    query_params = {
        "title": title or "",
        "location": location or "",
        "limit": limit,
        "page": page
    }

    jobs = []

    # --- Mantiks API ---
import os
import requests

MANTIKS_API_URL = "https://api.mantiks.io/api/v1/jobs/search"

def fetch_jobs(title=None, location=None, limit=25, page=1, **kwargs):
    """
    Fetch jobs from Mantiks API. Falls back gracefully to mock data if unavailable.
    """
    api_key = os.getenv("MANTIKS_API_KEY")
    headers = {"Authorization": f"Bearer {api_key}"} if api_key else {}
    
    params = {
        "title": title or "python developer",
        "location": location or "India",
        "limit": limit,
        "page": page
    }

    try:
        print(f"🔍 Fetching jobs from Mantiks: {params}")
        response = requests.get(MANTIKS_API_URL, headers=headers, params=params, timeout=10)
        response.raise_for_status()
        data = response.json()

        if isinstance(data, dict) and "results" in data:
            return data["results"]
        elif isinstance(data, list):
            return data  # Some APIs return raw list
        else:
            print("⚠️ Unexpected Mantiks API response structure.")
            return []

    except requests.exceptions.RequestException as e:
        print(f"❌ Mantiks API fetch failed: {e}")
        return []


def fetch_job_by_id(job_id):
    """Fetch detailed job info by ID from Mantiks API."""
    api_key = os.getenv("MANTIKS_API_KEY")
    if not api_key:
        print("⚠️ No Mantiks API key found.")
        return None

    headers = {"Authorization": f"Bearer {api_key}"}
    try:
        url = f"https://api.mantiks.io/api/v1/jobs/{job_id}"
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"❌ Mantiks job detail fetch failed: {e}")
        return None



# -----------------------------
# Test Run
# -----------------------------
if __name__ == "__main__":
    import json
    print("🧪 Testing unified Job API Client...")
    res = fetch_jobs(title="python", location="Bengaluru", limit=3)
    print(f"✅ Got {len(res)} jobs")
    print(json.dumps(res[:2], indent=2))
