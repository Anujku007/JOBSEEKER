import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    # Use a strong secret key
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'jobseeker-super-secret-key-2024-' + os.urandom(24).hex()
    
    # Database - use absolute path to avoid confusion
    BASE_DIR = os.path.abspath(os.path.dirname(__file__))
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or f'sqlite:///{os.path.join(BASE_DIR, "jobseeker.db")}'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    # Security
    WTF_CSRF_ENABLED = True
    WTF_CSRF_SECRET_KEY = os.environ.get('CSRF_SECRET_KEY') or 'csrf-super-secret-' + os.urandom(24).hex()
    
    # Session
    SESSION_PERMANENT = True
    PERMANENT_SESSION_LIFETIME = 3600  # 1 hour
    
    # Flask-Login
    REMEMBER_COOKIE_DURATION = 3600
    REMEMBER_COOKIE_SECURE = False  # Set to True in production with HTTPS
    
    # Database
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL', 'sqlite:///jobseeker.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    # Indian Job APIs
    ADZUNA_APP_ID = os.getenv('ADZUNA_APP_ID', '')
    ADZUNA_APP_KEY = os.getenv('ADZUNA_APP_KEY', '')
    
    # Adzuna India specific endpoint
    ADZUNA_INDIA_API = 'https://api.adzuna.com/v1/api/jobs/in/search/1'
    
    # Other potential Indian APIs
    GITHUB_JOBS_API = 'https://jobs.github.com/positions.json'
    RAPIDAPI_KEY = os.getenv('RAPIDAPI_KEY', '')
    
class DevelopmentConfig(Config):
    DEBUG = True

class ProductionConfig(Config):
    DEBUG = False

config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig
}