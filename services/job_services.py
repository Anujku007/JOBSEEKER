from services.api_service import ApiService
from services.saved_job_service import SavedJobService
from services.application_service import ApplicationService
from flask_login import current_user
from models.job import Job  # Import from the correct location
import datetime

class JobService:
    def __init__(self):
        self.api_service = ApiService()
        self.saved_job_service = SavedJobService()
        self.application_service = ApplicationService()

    def search_jobs(self, query='', location=''):
        """Search jobs from APIs or mock data"""
        try:
            # Get jobs from APIs
            api_jobs = self.api_service.get_all_jobs(query, location)
            
            # If no API jobs found, fall back to mock data
            if not api_jobs:
                api_jobs = self._get_mock_jobs()
            
            # Check if each job is saved and applied by current user
            for job in api_jobs:
                if current_user.is_authenticated:
                    job.is_saved = self.saved_job_service.is_job_saved(job.id)
                    job.is_applied = self.application_service.is_job_applied(job.id)
                else:
                    job.is_saved = False
                    job.is_applied = False
            
            return api_jobs
            
        except Exception as e:
            print(f"Error in search_jobs: {e}")
            # Fallback to mock data
            return self._get_mock_jobs()

    def _get_mock_jobs(self):
        """Get mock jobs for demonstration"""
        mock_jobs = [
            Job(
                id=1,
                title="Frontend Developer",
                company="TechCorp",
                location="Bangalore",
                job_type="Full-time",
                salary="₹8L - ₹12L",
                description="We are looking for a skilled Frontend Developer with React experience to join our team. You will be responsible for building user interfaces and implementing design systems.",
                url="https://example.com/job/1",
                posted_date=datetime.datetime.now().strftime("%Y-%m-%d"),
                remote=True,
                source="Mock Data"
            ),
            Job(
                id=2,
                title="Backend Engineer",
                company="StartupXYZ",
                location="Remote",
                job_type="Full-time",
                salary="₹10L - ₹15L",
                description="Join our backend team to build scalable APIs and services. Experience with Python, Flask, and database design required.",
                url="https://example.com/job/2",
                posted_date=datetime.datetime.now().strftime("%Y-%m-%d"),
                remote=True,
                source="Mock Data"
            ),
            Job(
                id=3,
                title="Full Stack Developer",
                company="DigitalSolutions",
                location="Delhi",
                job_type="Contract",
                salary="₹6L - ₹9L",
                description="Looking for a full stack developer with Python and JavaScript experience. Must have knowledge of frontend and backend technologies.",
                url="https://example.com/job/3",
                posted_date=datetime.datetime.now().strftime("%Y-%m-%d"),
                remote=False,
                source="Mock Data"
            )
        ]
        return mock_jobs

    def get_job_by_id(self, job_id):
        """Get job by ID from search results"""
        try:
            # Convert job_id to integer for comparison
            try:
                job_id_int = int(job_id)
            except ValueError:
                # If it's not an integer, try string comparison
                job_id_int = job_id
            
            # Search all jobs and find the one with matching ID
            all_jobs = self.search_jobs()
            for job in all_jobs:
                if str(job.id) == str(job_id):  # Compare as strings to be safe
                    return job
            
            # If not found in current search, try mock data directly
            mock_jobs = self._get_mock_jobs()
            for job in mock_jobs:
                if str(job.id) == str(job_id):
                    return job
                    
            return None
            
        except Exception as e:
            print(f"Error getting job by ID {job_id}: {e}")
            return None