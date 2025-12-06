# Routes package - centralized blueprint imports
from app.routes.auth import auth_bp
from app.routes.dashboard import dashboard_bp
from app.routes.halls import halls_bp
from app.routes.bookings import bookings_bp
from app.routes.api import api_bp
from app.routes.admin import admin_bp

__all__ = ['auth_bp', 'dashboard_bp', 'halls_bp', 'bookings_bp', 'api_bp', 'admin_bp']
