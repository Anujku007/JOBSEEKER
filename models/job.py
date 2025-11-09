class Job:
    """
    Job model to represent job listings from various sources
    This is a plain Python class (not a database model) for API jobs
    """
    
    def __init__(self, id, title, company, location, job_type, salary, description, url, posted_date, remote, source):
        self.id = id
        self.title = title
        self.company = company
        self.location = location
        self.job_type = job_type
        self.salary = salary
        self.description = description
        self.url = url
        self.posted_date = posted_date
        self.remote = remote
        self.source = source
        
        # These will be set later based on user actions
        self.is_saved = False
        self.is_applied = False

    def to_dict(self):
        """Convert job object to dictionary for JSON serialization"""
        return {
            'id': self.id,
            'title': self.title,
            'company': self.company,
            'location': self.location,
            'job_type': self.job_type,
            'salary': self.salary,
            'description': self.description,
            'url': self.url,
            'posted_date': self.posted_date,
            'remote': self.remote,
            'source': self.source,
            'is_saved': self.is_saved,
            'is_applied': self.is_applied
        }

    def __repr__(self):
        return f"<Job {self.id}: {self.title} at {self.company}>"