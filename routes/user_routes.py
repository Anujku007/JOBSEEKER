from flask import Blueprint, render_template, current_app, url_for
from flask_login import login_required, current_user
from models.simple_models import SavedJob, Application
import os

user_bp = Blueprint('user_bp', __name__)

# -----------------------------------------------------------
# 🏠 USER DASHBOARD
# -----------------------------------------------------------
@user_bp.route('/dashboard')
@login_required
def dashboard():
    """User dashboard showing saved jobs and applications"""
    try:
        saved_jobs = SavedJob.query.filter_by(user_id=current_user.id).all()
        applications = Application.query.filter_by(user_id=current_user.id).all()
        current_app.logger.info(f"📊 Dashboard loaded for {current_user.email}: {len(saved_jobs)} saved, {len(applications)} applied")

        return render_template('user/dashboard.html',
                               user=current_user,
                               saved_jobs=saved_jobs,
                               applications=applications)
    except Exception as e:
        current_app.logger.error(f"❌ Dashboard error: {e}")
        return render_template('user/dashboard.html',
                               user=current_user,
                               saved_jobs=[],
                               applications=[])

# -----------------------------------------------------------
# 👤 USER PROFILE
# -----------------------------------------------------------
@user_bp.route('/profile')
@login_required
def profile():
    """User profile page"""
    try:
        applications = Application.query.filter_by(user_id=current_user.id).all()
        saved_jobs = SavedJob.query.filter_by(user_id=current_user.id).all()
        return render_template('user/profile.html',
                               user=current_user,
                               applications=applications,
                               saved_jobs=saved_jobs)
    except Exception as e:
        current_app.logger.error(f"❌ Profile error: {e}")
        return render_template('user/profile.html', user=current_user)

# -----------------------------------------------------------
# 🧾 APPLICATIONS PAGE (Enhanced for Template Compatibility)
# -----------------------------------------------------------
@user_bp.route('/applications')
@login_required
def applications():
    """User's applications page (shows all applied jobs with details)"""
    try:
        applications = Application.query.filter_by(user_id=current_user.id).order_by(Application.applied_at.desc()).all()
        current_app.logger.info(f"📝 Found {len(applications)} applications for user {current_user.email}")

        enriched_apps = []
        for app in applications:
            enriched_apps.append({
                "id": app.id,
                "job_id": app.job_id,
                "job_title": app.job_title or "Untitled",
                "job_company": app.job_company or "Unknown Company",
                "job_location": app.job_location or "India",
                "job_type": app.job_type or "Full-time",
                "job_salary": app.job_salary or "Not specified",
                "job_description": app.job_description or "",
                "job_posted_date": app.job_posted_date or "Recently",
                "job_remote": bool(app.job_remote),
                "job_source": app.job_source or "N/A",
                "status": app.status or "Applied",
                "notes": app.notes or "",
                "resume_file": app.resume_file,
                "resume_path": (
                    url_for('jobs_bp.download_resume', filename=app.resume_file)
                    if app.resume_file else None
                ),
                "applied_at": app.applied_at
            })

        return render_template('user/applications.html', applications=enriched_apps)

    except Exception as e:
        current_app.logger.error(f"❌ Applications error: {e}")
        return render_template('user/applications.html', applications=[])
