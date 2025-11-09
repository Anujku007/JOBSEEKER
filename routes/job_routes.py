from rapidapi_client import fetch_jobs_from_rapidapi, _cache, get_job_by_id_from_cache
from flask import Blueprint, render_template, request, jsonify, current_app, send_from_directory, redirect, url_for
from flask_login import login_required, current_user
from werkzeug.utils import secure_filename
from extensions import db
from models.simple_models import SavedJob, Application
import os, random, time, re, uuid
from datetime import datetime, timedelta
from jobapi_client import fetch_jobs, fetch_job_by_id

# -----------------------------------------------
# 🔰 Blueprint
# -----------------------------------------------
jobs_bp = Blueprint("jobs_bp", __name__)

# -----------------------------------------------
# 🗺️ Indian City Normalization
# -----------------------------------------------
INDIAN_CITIES = {
    "delhi": "New Delhi", "new delhi": "New Delhi",
    "mumbai": "Mumbai", "bombay": "Mumbai",
    "bangalore": "Bengaluru", "banglore": "Bengaluru", "bengaluru": "Bengaluru",
    "chennai": "Chennai", "hyderabad": "Hyderabad", "pune": "Pune",
    "kolkata": "Kolkata", "gurgaon": "Gurugram", "gurugram": "Gurugram",
    "noida": "Noida", "ahmedabad": "Ahmedabad", "jaipur": "Jaipur",
    "lucknow": "Lucknow", "kochi": "Kochi", "indore": "Indore",
}

def normalize_location(city_name):
    if not city_name:
        return "India"
    city = city_name.strip().lower()
    return INDIAN_CITIES.get(city, city_name.title())

# -----------------------------------------------
# 💾 Fast Mock Job Generator (with caching)
# -----------------------------------------------
_mock_cache = {"timestamp": 0, "data": []}

def generate_mock_jobs(count=15):
    """Generate fake jobs if API fails."""
    global _mock_cache
    if time.time() - _mock_cache["timestamp"] < 60 and _mock_cache["data"]:
        current_app.logger.info("♻️ Using cached mock jobs.")
        return _mock_cache["data"]

    titles = [
        "Python Developer", "Full Stack Engineer", "Frontend Developer",
        "Backend Developer", "Data Scientist", "AI Engineer", "DevOps Engineer"
    ]
    companies = ["Tata Consultancy", "Infosys", "Tech Mahindra", "Wipro", "HCL", "Zoho"]
    locations = [
        "Bengaluru", "Hyderabad", "Pune", "Chennai", "Mumbai",
        "New Delhi", "Gurugram", "Noida", "Kolkata", "Ahmedabad", "Jaipur"
    ]

    jobs = []
    for i in range(count):
        days_ago = random.randint(1, 25)
        remote = random.choice([True, False])
        job = {
            "id": f"mock_{i+1}",
            "title": random.choice(titles),
            "company": random.choice(companies),
            "location": "Remote" if remote else random.choice(locations),
            "job_type": random.choice(["Full-time", "Contract", "Internship"]),
            "salary": f"₹{random.randint(4, 20)} LPA",
            "description": "Exciting opportunity to work with top Indian companies.",
            "url": f"/jobs/mock_{i+1}",
            "posted_date": (datetime.now() - timedelta(days=days_ago)).strftime("%b %d, %Y"),
            "remote": remote,
            "source": "MOCK",
        }
        jobs.append(job)

    _mock_cache["data"] = jobs
    _mock_cache["timestamp"] = time.time()
    current_app.logger.info("💾 Generated and cached fresh mock jobs.")
    return jobs

# -----------------------------------------------
# 🧩 Normalize API Job Data
# -----------------------------------------------
def normalize_api_job(api_job):
    """Convert Mantiks or RapidAPI response to a unified structure."""
    return {
        "id": str(api_job.get("id") or api_job.get("job_id") or api_job.get("url") or ""),
        "title": api_job.get("title") or "Untitled",
        "company": api_job.get("company") or "Unknown",
        "location": api_job.get("location") or "India",
        "job_type": api_job.get("type") or "Full-time",
        "salary": api_job.get("salary") or "",
        "description": api_job.get("description") or "",
        "url": api_job.get("url") or "",
        "posted_date": api_job.get("posted_on") or api_job.get("posted_date") or "Recently",
        "remote": bool(api_job.get("remote", False)),
        "source": api_job.get("source") or "API",
    }

# -----------------------------------------------
# ⚡ JOB LIST
# -----------------------------------------------
@jobs_bp.route("/")
def job_list():
    """Show job listings from Mantiks, RapidAPI, or fallback to mock data."""
    q = request.args.get("q")
    location = request.args.get("location")
    job_type = request.args.get("type")
    salary_min = request.args.get("salary_min")
    limit = int(request.args.get("limit", 25))
    normalized_location = normalize_location(location)

    current_app.logger.info(f"🔍 Searching jobs for '{q}' in '{normalized_location}'")
    jobs, data_source = [], "Mantiks"
    start_time = time.time()

    # 1️⃣ Mantiks API
    try:
        api_jobs = fetch_jobs(title=q, location=normalized_location, limit=limit, timeout=3)
        jobs = [normalize_api_job(j) for j in api_jobs] if api_jobs else []
        if not jobs:
            raise Exception("Empty Mantiks API result")
    except Exception as e:
        current_app.logger.warning(f"⚠️ Mantiks API failed: {e}")
        jobs = []

    # 2️⃣ RapidAPI fallback
    if not jobs:
        current_app.logger.info("🔁 Trying RapidAPI JSearch...")
        jobs = fetch_jobs_from_rapidapi(title=q, location=normalized_location, limit=limit)
        data_source = "RapidAPI" if jobs else "MOCK"
        if not jobs:
            jobs = generate_mock_jobs(limit)
            current_app.logger.info("💾 Using mock data (offline mode).")

    # 3️⃣ Apply filters
    if job_type:
        jobs = [j for j in jobs if job_type.lower() in (j.get("job_type") or "").lower()]
    if normalized_location.lower() != "india":
        jobs = [j for j in jobs if normalized_location.lower() in (j.get("location") or "").lower()]
    if salary_min:
        try:
            min_salary = int(salary_min)
            def parse_salary(s):
                match = re.search(r"(\d+)", s.replace(",", ""))
                return int(match.group(1)) if match else 0
            jobs = [j for j in jobs if parse_salary(j.get("salary", "0")) >= min_salary]
        except Exception:
            pass

    # 4️⃣ Mark saved/applied jobs
    if current_user.is_authenticated:
        saved_ids = {s.job_id for s in SavedJob.query.filter_by(user_id=current_user.id)}
        applied_ids = {a.job_id for a in Application.query.filter_by(user_id=current_user.id)}
        for j in jobs:
            j["is_saved"] = j["id"] in saved_ids
            j["is_applied"] = j["id"] in applied_ids
    else:
        for j in jobs:
            j["is_saved"] = j["is_applied"] = False

    total_time = round(time.time() - start_time, 2)
    current_app.logger.info(f"⚡ Job fetch completed in {total_time}s from {data_source}")

    return render_template(
        "jobs/list.html",
        jobs=jobs,
        search_query=q or "",
        location=normalized_location,
        job_type=job_type or "",
        salary_min=salary_min or "",
        using_api=(data_source != "MOCK"),
    )

# -----------------------------------------------
# 🧾 JOB DETAIL
# -----------------------------------------------
@jobs_bp.route("/<path:job_id>")
def job_detail(job_id):
    """Show detailed job info (Mantiks → RapidAPI → DB → Mock)."""
    current_app.logger.info(f"🔎 Loading job details for ID: {job_id}")

    # 1️⃣ Mantiks API
    try:
        job = fetch_job_by_id(job_id)
        if job:
            job["source"] = "Mantiks"
            return render_template("jobs/detail.html", job=job)
    except Exception as e:
        current_app.logger.warning(f"❌ Mantiks job detail fetch failed: {e}")

    # 2️⃣ RapidAPI cache lookup
    try:
        cached_job = get_job_by_id_from_cache(job_id)
        if cached_job:
            current_app.logger.info(f"♻️ Found RapidAPI job from cache: {job_id}")
            return render_template("jobs/detail.html", job=cached_job)
        if _cache.get("data"):
            match = next((j for j in _cache["data"] if str(j.get("id")) == str(job_id)), None)
            if match:
                current_app.logger.info(f"♻️ Found RapidAPI job in list cache: {job_id}")
                return render_template("jobs/detail.html", job=match)
    except Exception as e:
        current_app.logger.warning(f"⚠️ RapidAPI cache lookup failed: {e}")

    # 3️⃣ Saved job fallback
    if current_user.is_authenticated:
        saved = SavedJob.query.filter_by(user_id=current_user.id, job_id=job_id).first()
        if saved:
            job = {
                "id": saved.job_id,
                "title": saved.job_title,
                "company": saved.job_company,
                "location": saved.job_location,
                "salary": saved.job_salary,
                "description": saved.job_description,
                "url": saved.job_url,
                "source": saved.job_source or "Saved",
            }
            return render_template("jobs/detail.html", job=job)

    # 4️⃣ Mock fallback
    job = next((j for j in generate_mock_jobs() if str(j["id"]) == str(job_id)), None)
    if job:
        job["source"] = "Mock"
        return render_template("jobs/detail.html", job=job)

    return render_template("404.html", message="Job not found or unavailable."), 404

# -----------------------------------------------
# 📝 APPLY JOB
# -----------------------------------------------
@jobs_bp.route("/<path:job_id>/apply", methods=["GET", "POST"])
@login_required
def apply_job(job_id):
    """Handle job applications with resume upload."""
    if request.method == "GET":
        job = (
            fetch_job_by_id(job_id)
            or get_job_by_id_from_cache(job_id)
            or next((j for j in generate_mock_jobs() if j["id"] == job_id), None)
        )
        if not job:
            return render_template("404.html", message="Job not found."), 404
        return render_template("jobs/apply_form.html", job=job)

    try:
        name = request.form.get("name")
        email = request.form.get("email")
        phone = request.form.get("phone")
        cover_letter = request.form.get("cover_letter", "")
        resume = request.files.get("resume")

        if not name or not email:
            return jsonify({"success": False, "message": "Name and Email are required!"}), 400

        if Application.query.filter_by(user_id=current_user.id, job_id=job_id).first():
            return jsonify({"success": False, "message": "⚠️ You already applied to this job."})

        # 📎 Resume upload
        resume_filename = None
        if resume:
            allowed_ext = {".pdf", ".doc", ".docx"}
            ext = os.path.splitext(resume.filename)[1].lower()
            if ext not in allowed_ext:
                return jsonify({"success": False, "message": "Invalid file type."}), 400
            if resume.content_length and resume.content_length > 5 * 1024 * 1024:
                return jsonify({"success": False, "message": "File too large (max 5MB)."}), 400

            upload_folder = os.path.join(current_app.root_path, "uploads", "resumes")
            os.makedirs(upload_folder, exist_ok=True)
            resume_filename = secure_filename(f"{current_user.id}_{uuid.uuid4().hex}{ext}")
            resume.save(os.path.join(upload_folder, resume_filename))

        job = fetch_job_by_id(job_id) or get_job_by_id_from_cache(job_id) or {"title": "Untitled", "company": "Unknown"}

        application = Application(
            user_id=current_user.id,
            job_id=job_id,
            job_title=job.get("title", "Untitled"),
            job_company=job.get("company", "Unknown"),
            job_location=job.get("location", ""),
            job_salary=job.get("salary", ""),
            job_description=job.get("description", ""),
            job_url=job.get("url", ""),
            job_posted_date=job.get("posted_date", ""),
            job_source=job.get("source", "Mock"),
            status="Applied",
            notes=cover_letter,
            resume_file=resume_filename,
        )
        db.session.add(application)
        db.session.commit()

        current_app.logger.info(f"✅ Application submitted for {current_user.email}")

        # Return success
        if request.accept_mimetypes.accept_html:
            return redirect(url_for("user_bp.applications"))
        return jsonify({"success": True, "message": "✅ Application submitted successfully!"}), 200

    except Exception as e:
        db.session.rollback()
        current_app.logger.error(f"❌ Error applying job {job_id}: {e}")
        return jsonify({"success": False, "message": "❌ Server error, please try again later."}), 500

# -----------------------------------------------
# ❤️ SAVE / UNSAVE JOB
# -----------------------------------------------
@jobs_bp.route("/<path:job_id>/save", methods=["POST"])
@login_required
def save_job(job_id):
    try:
        existing = SavedJob.query.filter_by(user_id=current_user.id, job_id=job_id).first()
        if existing:
            db.session.delete(existing)
            db.session.commit()
            return jsonify({"success": True, "message": "Job removed from saved list."})

        job = (
            fetch_job_by_id(job_id)
            or get_job_by_id_from_cache(job_id)
            or next((j for j in generate_mock_jobs() if j["id"] == job_id), None)
            or {"title": "Untitled", "company": "Unknown", "location": "India"}
        )

        new_saved = SavedJob(
            user_id=current_user.id,
            job_id=job_id,
            job_title=job.get("title"),
            job_company=job.get("company"),
            job_location=job.get("location"),
            job_salary=job.get("salary", ""),
            job_description=job.get("description", ""),
            job_url=job.get("url", ""),
            job_source=job.get("source", "RapidAPI")
        )
        db.session.add(new_saved)
        db.session.commit()
        return jsonify({"success": True, "message": "Job saved successfully!"})
    except Exception as e:
        db.session.rollback()
        current_app.logger.error(f"❌ Error saving job {job_id}: {e}")
        return jsonify({"success": False, "message": "Failed to save job."}), 500

@jobs_bp.route("/<path:job_id>/unsave", methods=["POST"])
@login_required
def unsave_job(job_id):
    saved = SavedJob.query.filter_by(user_id=current_user.id, job_id=job_id).first()
    if not saved:
        return jsonify({"success": False, "message": "Job not found in saved list."})
    db.session.delete(saved)
    db.session.commit()
    return jsonify({"success": True, "message": "Job removed from saved list."})

# -----------------------------------------------
# ⭐ SAVED JOBS PAGE
# -----------------------------------------------
@jobs_bp.route("/saved")
@login_required
def saved_jobs():
    saved = SavedJob.query.filter_by(user_id=current_user.id).all()
    return render_template("jobs/saved.html", saved_jobs=saved)

# -----------------------------------------------
# 📎 DOWNLOAD RESUME
# -----------------------------------------------
@jobs_bp.route("/resumes/<filename>")
@login_required
def download_resume(filename):
    resume_path = os.path.join(current_app.root_path, "uploads", "resumes")
    return send_from_directory(resume_path, filename, as_attachment=True)
