from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify
from flask_login import login_required, current_user
from app import db
from app.models import Booking, Hall, User, StaffLog
from app.utils import admin_required
from datetime import datetime, timedelta

dashboard_bp = Blueprint('dashboard', __name__, url_prefix='/dashboard')

@dashboard_bp.route('/', methods=['GET'])
@login_required
def index():
    if current_user.is_admin():
        return redirect(url_for('admin.dashboard'))
    return redirect(url_for('dashboard.staff_dashboard'))

@dashboard_bp.route('/staff', methods=['GET'])
@login_required
def staff_dashboard():
    if current_user.is_admin():
        return redirect(url_for('admin.dashboard'))
    
    today = datetime.now().date()
    
    # Today's bookings created by current staff
    today_bookings = Booking.query.filter_by(
        created_by=current_user.id,
        date=today
    ).order_by(Booking.start_time).all()
    
    # Upcoming bookings
    upcoming_bookings = Booking.query.filter(
        Booking.created_by == current_user.id,
        Booking.date >= today,
        Booking.status != 'cancelled'
    ).order_by(Booking.date, Booking.start_time).limit(5).all()
    
    # Available halls
    available_halls = Hall.query.filter_by(status='active').all()
    
    return render_template('dashboard/staff.html',
                         today_bookings=today_bookings,
                         upcoming_bookings=upcoming_bookings,
                         available_halls=available_halls)
