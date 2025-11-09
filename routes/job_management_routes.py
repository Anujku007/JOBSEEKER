from flask import Blueprint, render_template, request, jsonify
from flask_login import login_required, current_user
from models import SavedJob, Application, Job, db
from datetime import datetime

job_management_bp = Blueprint('job_management', __name__)

@job_management_bp.route('/save-job/<int:job_id>', methods=['POST'])
@login_required
def save_job(job_id):
    job = Job.query.get_or_404(job_id)
    
    # Check if already saved
    existing_save = SavedJob.query.filter_by(user_id=current_user.id, job_id=job_id).first()
    
    if existing_save:
        db.session.delete(existing_save)
        db.session.commit()
        return jsonify({'saved': False, 'message': 'Job removed from saved jobs'})
    else:
        saved_job = SavedJob(user_id=current_user.id, job_id=job_id)
        db.session.add(saved_job)
        db.session.commit()
        return jsonify({'saved': True, 'message': 'Job saved successfully'})

@job_management_bp.route('/apply-job/<int:job_id>', methods=['POST'])
@login_required
def apply_job(job_id):
    job = Job.query.get_or_404(job_id)
    cover_letter = request.form.get('cover_letter', '')
    
    # Check if already applied
    existing_application = Application.query.filter_by(
        user_id=current_user.id, 
        job_id=job_id
    ).first()
    
    if existing_application:
        return jsonify({'success': False, 'message': 'You have already applied to this job'})
    
    # Create new application
    application = Application(
        user_id=current_user.id,
        job_id=job_id,
        cover_letter=cover_letter,
        applied_at=datetime.utcnow()
    )
    
    db.session.add(application)
    db.session.commit()
    
    return jsonify({'success': True, 'message': 'Application submitted successfully'})

@job_management_bp.route('/saved-jobs')
@login_required
def saved_jobs():
    saved_jobs = SavedJob.query.filter_by(user_id=current_user.id).all()
    jobs = [saved_job.job for saved_job in saved_jobs]
    return render_template('job/saved_jobs.html', jobs=jobs)

@job_management_bp.route('/applications')
@login_required
def applications():
    applications = Application.query.filter_by(user_id=current_user.id).order_by(Application.applied_at.desc()).all()
    return render_template('job/applications.html', applications=applications)

@job_management_bp.route('/dashboard')
@login_required
def dashboard():
    # Get user stats
    saved_count = SavedJob.query.filter_by(user_id=current_user.id).count()
    applications_count = Application.query.filter_by(user_id=current_user.id).count()
    
    # Get recent applications
    recent_applications = Application.query.filter_by(
        user_id=current_user.id
    ).order_by(Application.applied_at.desc()).limit(5).all()
    
    # Get recommended jobs (simplified - you can implement better recommendation logic)
    recommended_jobs = Job.query.limit(6).all()
    
    return render_template('dashboard.html',
                         saved_count=saved_count,
                         applications_count=applications_count,
                         recent_applications=recent_applications,
                         recommended_jobs=recommended_jobs)