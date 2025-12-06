from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
from app import db

class User(UserMixin, db.Model):
    """User model for staff and admin"""
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False, index=True)
    password_hash = db.Column(db.String(255), nullable=False)
    role = db.Column(db.String(20), nullable=False, default='staff')  # admin or staff
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    is_active = db.Column(db.Boolean, nullable=False, default=True)
    
    # Relationships
    bookings = db.relationship('Booking', backref='created_by_user', lazy=True, foreign_keys='Booking.created_by')
    logs = db.relationship('StaffLog', backref='user', lazy=True)
    
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)
    
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)
    
    def is_admin(self):
        return self.role == 'admin'
    
    def __repr__(self):
        return f'<User {self.username}>'


class Hall(db.Model):
    """Hall model for booking halls"""
    __tablename__ = 'halls'
    
    id = db.Column(db.Integer, primary_key=True)
    hall_name = db.Column(db.String(120), nullable=False, index=True)
    description = db.Column(db.Text, nullable=True)
    capacity = db.Column(db.Integer, nullable=False)
    price = db.Column(db.Float, nullable=False)
    working_from = db.Column(db.String(5), nullable=False, default='09:00')  # HH:MM
    working_to = db.Column(db.String(5), nullable=False, default='22:00')    # HH:MM
    image = db.Column(db.String(255), nullable=True)
    status = db.Column(db.String(20), nullable=False, default='active')  # active or disabled
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    
    # Relationships
    bookings = db.relationship('Booking', backref='hall', lazy=True, cascade='all, delete-orphan')
    
    def __repr__(self):
        return f'<Hall {self.hall_name}>'


class Booking(db.Model):
    """Booking model for hall bookings"""
    __tablename__ = 'bookings'
    
    id = db.Column(db.Integer, primary_key=True)
    hall_id = db.Column(db.Integer, db.ForeignKey('halls.id'), nullable=False, index=True)
    customer_name = db.Column(db.String(120), nullable=False)
    phone = db.Column(db.String(20), nullable=False)
    phone_alt = db.Column(db.String(20), nullable=True)
    date = db.Column(db.Date, nullable=False, index=True)
    start_time = db.Column(db.String(5), nullable=False)  # HH:MM
    end_time = db.Column(db.String(5), nullable=False)    # HH:MM
    deposit = db.Column(db.Float, nullable=False, default=0)
    total_price = db.Column(db.Float, nullable=False)
    status = db.Column(db.String(20), nullable=False, default='pending')  # pending, approved, completed, cancelled
    notes = db.Column(db.Text, nullable=True)
    # Selected add-ons stored as JSON list: [{"name":"كوشة","price":200,"note":"..."}, ...]
    addons = db.Column(db.JSON, nullable=True)
    created_by = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def __repr__(self):
        return f'<Booking {self.customer_name} - {self.date}>'


class Addon(db.Model):
    """Addon catalog for optional services"""
    __tablename__ = 'addons'

    id = db.Column(db.Integer, primary_key=True)
    code = db.Column(db.String(50), unique=True, nullable=False, index=True)
    name = db.Column(db.String(120), nullable=False)
    description = db.Column(db.Text, nullable=True)
    icon = db.Column(db.String(80), nullable=True)
    price = db.Column(db.Float, nullable=False, default=0)
    active = db.Column(db.Boolean, nullable=False, default=True)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow, onupdate=datetime.utcnow)

    def to_dict(self):
        return {
            'id': self.id,
            'code': self.code,
            'name': self.name,
            'desc': self.description or '',
            'icon': self.icon or '',
            'price': self.price,
            'active': self.active,
        }

    def __repr__(self):
        return f'<Addon {self.code}>'


class StaffLog(db.Model):
    """Staff activity log model"""
    __tablename__ = 'staff_logs'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False, index=True)
    action = db.Column(db.String(50), nullable=False)  # login, logout, create_booking, edit_booking, etc
    details = db.Column(db.Text, nullable=True)
    timestamp = db.Column(db.DateTime, nullable=False, default=datetime.utcnow, index=True)
    
    def __repr__(self):
        return f'<StaffLog {self.user_id} - {self.action}>'
