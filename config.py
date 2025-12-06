"""
Application Configuration File
ملف إعدادات التطبيق
"""

import os

class Config:
    """Base configuration"""
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'elsafa-halls-secret-key-2025'
    
    # Database URI - supports both SQLite (local) and PostgreSQL (production)
    database_url = os.environ.get('DATABASE_URL')
    if database_url and database_url.startswith('postgres://'):
        # Render uses postgres:// but SQLAlchemy needs postgresql://
        database_url = database_url.replace('postgres://', 'postgresql://', 1)
    SQLALCHEMY_DATABASE_URI = database_url or 'sqlite:///elsafa_halls.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    # Session
    PERMANENT_SESSION_LIFETIME = 604800  # 7 days in seconds
    SESSION_COOKIE_HTTPONLY = True
    SESSION_COOKIE_SECURE = False  # Set to True in production with HTTPS
    SESSION_COOKIE_SAMESITE = 'Lax'
    
    # Pagination
    ITEMS_PER_PAGE = 10
    
    # Upload
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16MB max file size
    UPLOAD_FOLDER = os.path.join(os.path.dirname(__file__), 'static/uploads')
    
    # Application Info
    APP_NAME = 'Safa Downtown Halls'
    APP_VERSION = '1.0.0'
    COMPANY_NAME = 'Safa Downtown Halls'
    
    # System Configuration
    TIMEZONE = 'Asia/Riyadh'
    LANGUAGE = 'ar'
    
    # Feature Flags
    ENABLE_CSV_EXPORT = True
    ENABLE_EMAIL_NOTIFICATIONS = False
    ENABLE_SMS_NOTIFICATIONS = False
    ENABLE_REGISTRATION = False  # Staff registration disabled
    
    # Working Days (0 = Sunday, 6 = Saturday)
    WORKING_DAYS = [0, 1, 2, 3, 4, 5]  # Sunday to Friday
    
    # Global Add-ons (apply to all bookings, not tied to halls)
    AVAILABLE_ADDONS = [
        {'id': 'fire', 'name': 'العرض الناري', 'price': 1500, 'desc': 'صواريخ وFireworks', 'icon': 'fa-solid fa-rocket'},
        {'id': 'kosha', 'name': 'الكوشة', 'price': 800, 'desc': 'كوشة كاملة للعرسان', 'icon': 'fa-solid fa-couch'},
        {'id': 'curtains', 'name': 'الستائر', 'price': 600, 'desc': 'ديكور وستائر', 'icon': 'fa-solid fa-scroll'},
        {'id': 'laser', 'name': 'عرض ليزر', 'price': 1000, 'desc': 'إضاءات ليزر ملونة', 'icon': 'fa-solid fa-bolt'},
        {'id': 'led', 'name': 'شاشة ليد', 'price': 2000, 'desc': 'LED Screen للعروض', 'icon': 'fa-solid fa-tv'},
        {'id': 'audio', 'name': 'الصوتيات', 'price': 500, 'desc': 'سماعات وميكروفونات', 'icon': 'fa-solid fa-microphone'}
    ]


class DevelopmentConfig(Config):
    """Development configuration"""
    DEBUG = True
    TESTING = False


class ProductionConfig(Config):
    """Production configuration"""
    DEBUG = False
    TESTING = False
    SESSION_COOKIE_SECURE = True
    SESSION_COOKIE_HTTPONLY = True


class TestingConfig(Config):
    """Testing configuration"""
    DEBUG = True
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'


# Select configuration based on environment
config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'testing': TestingConfig,
    'default': DevelopmentConfig
}
