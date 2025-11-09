from extensions import db
from models.simple_models import Application
from flask_login import current_user

class ApplicationService:
    def apply_to_job(self, job_id, notes=None):
        """Apply to a job for the current user"""
        try:
            print(f"🔍 Applying to job {job_id} for user {current_user.id}")
            
            # Check if already applied
            existing_application = Application.query.filter_by(
                user_id=current_user.id,
                job_id=job_id
            ).first()
            
            if existing_application:
                print(f"❌ User already applied to job {job_id}")
                return {'success': False, 'message': 'You have already applied to this job'}

            # For now, use placeholder job data
            # In a real app, you would get this from your job service
            application = Application(
                user_id=current_user.id,
                job_id=job_id,
                job_title="Software Developer",  # Placeholder
                job_company="Tech Company",      # Placeholder  
                job_location="Remote",
                job_type="Full-time",
                job_salary="Competitive",
                job_description="Job description not available",
                job_url="#",
                job_posted_date="Recently",
                job_remote=True,
                job_source="JOBSEEKER",
                notes=notes
            )
            
            db.session.add(application)
            db.session.commit()
            print(f"✅ Application created for job {job_id}")
            return {'success': True, 'message': 'Application submitted successfully!'}
            
        except Exception as e:
            db.session.rollback()
            print(f"❌ Application error: {e}")
            return {'success': False, 'message': f'Error applying to job: {str(e)}'}

    def get_user_applications(self, user_id):
        """Get all job applications for a user"""
        try:
            applications = Application.query.filter_by(user_id=user_id).order_by(Application.applied_at.desc()).all()
            return [app.to_dict() for app in applications]
        except Exception as e:
            print(f"Error getting applications: {e}")
            return []

    def is_job_applied(self, job_id):
        """Check if current user has applied to this job"""
        if not current_user.is_authenticated:
            return False
            
        application = Application.query.filter_by(
            user_id=current_user.id,
            job_id=job_id
        ).first()
        
        return application is not None

    def get_application_status(self, job_id):
        """Check if the current user has applied to a job"""
        return self.is_job_applied(job_id)