from models.job import Job
import requests
import os
from datetime import datetime

class ApiService:
    def __init__(self):
        self.adzuna_app_id = os.environ.get('ADZUNA_APP_ID', '')
        self.adzuna_app_key = os.environ.get('ADZUNA_APP_KEY', '')
    
    def get_all_jobs(self, query='', location=''):
        """Get jobs from all available APIs"""
        jobs = []
        
        # Try Adzuna API first
        adzuna_jobs = self.get_adzuna_jobs(query, location)
        if adzuna_jobs:
            jobs.extend(adzuna_jobs)
        
        # If no jobs found, return empty list (will fall back to mock data)
        return jobs
    
    def get_adzuna_jobs(self, query='', location=''):
        """Get jobs from Adzuna API for India"""
        try:
            # For now, return empty list (we'll implement API later)
            # This allows fallback to mock data
            return []
            
        except Exception as e:
            print(f"Adzuna API error: {e}")
            return []
    
    def get_github_jobs(self, query='', location=''):
        """Get jobs from GitHub Jobs API"""
        try:
            # GitHub Jobs API is deprecated, return empty
            return []
        except Exception as e:
            print(f"GitHub Jobs API error: {e}")
            return []
    
    def get_remoteok_jobs(self, query=''):
        """Get jobs from RemoteOK API"""
        try:
            # Return empty for now
            return []
        except Exception as e:
            print(f"RemoteOK API error: {e}")
            return []