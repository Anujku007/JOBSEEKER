import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class Config:
    # -------------------------------------------------------
    # Security Keys
    # -------------------------------------------------------
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'jobseeker-super-secret-key-2024-' + os.urandom(24).hex()
    WTF_CSRF_ENABLED = True
    WTF_CSRF_SECRET_KEY = os.environ.get('CSRF_SECRET_KEY') or 'csrf-super-secret-' + os.urandom(24).hex()

    # -------------------------------------------------------
    # Base Directory
    # -------------------------------------------------------
    BASE_DIR = os.path.abspath(os.path.dirname(__file__))

    # -------------------------------------------------------
    # Database Configuration
    # -------------------------------------------------------
    # Use a writable location for SQLite on Render
    if os.getenv("RENDER") == "true":
        DB_PATH = os.path.join("/tmp", "jobseeker.db")
    else:
        DB_PATH = os.path.join(BASE_DIR, "jobseeker.db")

    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL') or f"sqlite:///{DB_PATH}"
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # -------------------------------------------------------
    # Session & Login Settings
    # -------------------------------------------------------
    SESSION_PERMANENT = True
    PERMANENT_SESSION_LIFETIME = 3600  # 1 hour
    REMEMBER_COOKIE_DURATION = 3600
    REMEMBER_COOKIE_SECURE = False  # True if using HTTPS

    # -------------------------------------------------------
    # Indian Job API Integrations
    # -------------------------------------------------------
    ADZUNA_APP_ID = os.getenv('ADZUNA_APP_ID', '')
    ADZUNA_APP_KEY = os.getenv('ADZUNA_APP_KEY', '')
    ADZUNA_INDIA_API = 'https://api.adzuna.com/v1/api/jobs/in/search/1'

    GITHUB_JOBS_API = 'https://jobs.github.com/positions.json'
    RAPIDAPI_KEY = os.getenv('RAPIDAPI_KEY', '')
    MANTIKS_API_KEY = os.getenv('MANTIKS_API_KEY', '')


class DevelopmentConfig(Config):
    DEBUG = True


class ProductionConfig(Config):
    DEBUG = False


config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig
}
