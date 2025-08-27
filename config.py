
import os
from datetime import timedelta

class Config:
    """Application configuration settings"""

    # Basic Flask configuration
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'comprehensive-predictive-modeling-platform-2025'

    # Database configuration
    DATABASE_URL = os.environ.get('DATABASE_URL') or 'sqlite:///comprehensive_analysis.db'

    # External API configuration
    OPENAI_API_KEY = os.environ.get('OPENAI_API_KEY') or ''

    # Application settings
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16MB max file upload

    # Session configuration
    PERMANENT_SESSION_LIFETIME = timedelta(hours=24)

    # Analysis configuration
    MAX_CONCURRENT_ANALYSES = 5
    ANALYSIS_TIMEOUT_SECONDS = 300  # 5 minutes

    # Visualization configuration
    MAX_VISUALIZATION_POINTS = 10000
    DEFAULT_MAP_PROJECTION = 'mercator'

    # Security configuration
    WTF_CSRF_ENABLED = True
    WTF_CSRF_TIME_LIMIT = None

    # Performance configuration
    CACHE_TYPE = 'simple'
    CACHE_DEFAULT_TIMEOUT = 300

    # Logging configuration
    LOG_LEVEL = os.environ.get('LOG_LEVEL') or 'INFO'
    LOG_FORMAT = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'

    @staticmethod
    def init_app(app):
        """Initialize application with configuration"""
        pass

class DevelopmentConfig(Config):
    """Development configuration"""
    DEBUG = True
    TESTING = False

class ProductionConfig(Config):
    """Production configuration"""
    DEBUG = False
    TESTING = False

    # Enhanced security for production
    SESSION_COOKIE_SECURE = True
    SESSION_COOKIE_HTTPONLY = True
    SESSION_COOKIE_SAMESITE = 'Lax'

class TestingConfig(Config):
    """Testing configuration"""
    TESTING = True
    WTF_CSRF_ENABLED = False
    DATABASE_URL = 'sqlite:///:memory:'

config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'testing': TestingConfig,
    'default': DevelopmentConfig
}
