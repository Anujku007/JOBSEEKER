from flask import Blueprint, render_template, jsonify, request
from flask_login import login_required, current_user
from services.saved_service import SavedJobService

saved_bp = Blueprint('saved', __name__)
saved_service = SavedJobService()

@saved_bp.route('/saved')
@login_required
def saved_jobs():
    """Display user's saved jobs"""
    saved_jobs = saved_service.get_saved_jobs(current_user.id)
    return render_template('saved_jobs.html', saved_jobs=saved_jobs)

@saved_bp.route('/api/save/<int:job_id>', methods=['POST'])
@login_required
def save_job(job_id):
    """API endpoint to save a job"""
    success, message = saved_service.save_job(current_user.id, job_id)
    return jsonify({
        'success': success,
        'message': message,
        'saved': success
    })

@saved_bp.route('/api/unsave/<int:job_id>', methods=['POST'])
@login_required
def unsave_job(job_id):
    """API endpoint to unsave a job"""
    success, message = saved_service.unsave_job(current_user.id, job_id)
    return jsonify({
        'success': success,
        'message': message,
        'saved': not success
    })

@saved_bp.route('/api/check-saved/<int:job_id>')
@login_required
def check_saved(job_id):
    """API endpoint to check if job is saved"""
    is_saved = saved_service.is_job_saved(current_user.id, job_id)
    return jsonify({
        'saved': is_saved
    })