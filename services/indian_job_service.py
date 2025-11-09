import requests
import json
from datetime import datetime
from models.simple_models import Job
from config import Config

class IndianJobService:
    def __init__(self):
        self.config = Config()
    
    def fetch_adzuna_india_jobs(self, query='', location=''):
        """Fetch jobs from Adzuna India API"""
        try:
            params = {
                'app_id': self.config.ADZUNA_APP_ID,
                'app_key': self.config.ADZUNA_APP_KEY,
                'what': query or 'developer',
                'where': location or 'india',
                'max_days_old': 30,
                'content-type': 'application/json'
            }
            
            response = requests.get(self.config.ADZUNA_INDIA_API, params=params, timeout=10)
            response.raise_for_status()
            
            data = response.json()
            jobs = []
            
            for job_data in data.get('results', []):
                job = Job(
                    title=job_data.get('title', ''),
                    company=job_data.get('company', {}).get('display_name', ''),
                    location=job_data.get('location', {}).get('display_name', ''),
                    job_type=job_data.get('contract_type', 'full-time'),  # Changed to job_type
                    salary=self._format_salary(job_data.get('salary_min'), job_data.get('salary_max')),
                    description=job_data.get('description', '')[:500],
                    url=job_data.get('redirect_url', '#'),
                    posted_date=job_data.get('created', ''),
                    remote=job_data.get('location', {}).get('area', []) == ['remote'] or 
                           'remote' in job_data.get('title', '').lower(),
                    source='Adzuna India'
                )
                jobs.append(job)
            
            return jobs
            
        except Exception as e:
            print(f"Error fetching Adzuna India jobs: {e}")
            return []
    
    def _format_salary(self, min_salary, max_salary):
        """Format salary range for display in INR"""
        if min_salary and max_salary:
            return f"₹{min_salary:,} - ₹{max_salary:,} per year"
        elif min_salary:
            return f"₹{min_salary:,} per year"
        elif max_salary:
            return f"₹{max_salary:,} per year"
        return "Salary not specified"
    
    def fetch_github_jobs_india(self, query='', location=''):
        """Fetch India-focused jobs from GitHub API"""
        try:
            params = {}
            if query:
                params['description'] = query
            if location:
                params['location'] = f"{location}, India"
            else:
                params['location'] = 'India'
            
            response = requests.get(self.config.GITHUB_JOBS_API, params=params, timeout=10)
            response.raise_for_status()
            
            jobs_data = response.json()
            jobs = []
            
            for job_data in jobs_data:
                job_location = job_data.get('location', '').lower()
                if 'india' in job_location or any(city in job_location for city in 
                   ['bangalore', 'delhi', 'mumbai', 'chennai', 'hyderabad', 'pune', 'kolkata']):
                    
                    job = Job(
                        title=job_data.get('title', ''),
                        company=job_data.get('company', ''),
                        location=job_data.get('location', ''),
                        job_type='full-time',  # Changed to job_type
                        salary=None,
                        description=job_data.get('description', '')[:500],
                        url=job_data.get('url', '#'),
                        posted_date=job_data.get('created_at', ''),
                        remote='remote' in job_data.get('title', '').lower() or 
                               'remote' in job_data.get('location', '').lower(),
                        source='GitHub Jobs India'
                    )
                    jobs.append(job)
            
            return jobs
            
        except Exception as e:
            print(f"Error fetching GitHub India jobs: {e}")
            return []
    
    def get_indian_jobs(self, query='', location=''):
        """Get jobs from all Indian sources"""
        all_jobs = []
        
        # Fetch from Adzuna India
        adzuna_jobs = self.fetch_adzuna_india_jobs(query, location)
        all_jobs.extend(adzuna_jobs)
        
        # Fetch from GitHub Jobs (India focused)
        github_jobs = self.fetch_github_jobs_india(query, location)
        all_jobs.extend(github_jobs)
        
        return all_jobs