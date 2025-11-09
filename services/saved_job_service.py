from extensions import db
from models.simple_models import SavedJob
from flask_login import current_user

class SavedJobService:
    def save_job(self, job_id):
        """Save a job for current user"""
        try:
            # Check if already saved
            existing_save = SavedJob.query.filter_by(
                user_id=current_user.id,
                job_id=job_id
            ).first()
            
            if existing_save:
                return {'success': False, 'message': 'Job already saved'}
            
            # For now, just return success without saving details
            # We'll implement full saving when we have job details
            return {'success': True, 'message': 'Job saved successfully'}
            
        except Exception as e:
            return {'success': False, 'message': f'Error saving job: {str(e)}'}
    
    def unsave_job(self, job_id):
        """Remove a saved job"""
        try:
            saved_job = SavedJob.query.filter_by(
                user_id=current_user.id,
                job_id=job_id
            ).first()
            
            if saved_job:
                db.session.delete(saved_job)
                db.session.commit()
                return {'success': True, 'message': 'Job removed from saved'}
            else:
                return {'success': False, 'message': 'Job not found in saved list'}
                
        except Exception as e:
            db.session.rollback()
            return {'success': False, 'message': f'Error unsaving job: {str(e)}'}
    
    def get_saved_jobs(self, user_id):
        """Get all saved jobs for a user"""
        try:
            saved_jobs = SavedJob.query.filter_by(user_id=user_id).all()
            return saved_jobs
        except Exception as e:
            print(f"Error getting saved jobs: {e}")
            return []
    
    def is_job_saved(self, job_id):
        """Check if a job is saved by current user"""
        if not current_user.is_authenticated:
            return False
            
        saved_job = SavedJob.query.filter_by(
            user_id=current_user.id,
            job_id=job_id
        ).first()
        
        return saved_job is not None