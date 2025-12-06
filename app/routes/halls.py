from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify
from flask_login import login_required, current_user
from app import db
from app.models import Booking, Hall, StaffLog
from app.utils import admin_required
from datetime import datetime, timedelta
from calendar import monthrange
import json
from datetime import date as _date

halls_bp = Blueprint('halls', __name__, url_prefix='/halls')

@halls_bp.route('/', methods=['GET'])
@login_required
def list_halls():
    """List all active halls"""
    halls = Hall.query.filter_by(status='active').all()
    return render_template('halls/list.html', halls=halls)

@halls_bp.route('/manage', methods=['GET'])
@login_required
@admin_required
def manage_halls():
    """Manage halls (Admin only)"""
    halls = Hall.query.all()
    return render_template('halls/manage.html', halls=halls)

@halls_bp.route('/add', methods=['GET', 'POST'])
@login_required
@admin_required
def add_hall():
    """Add new hall (Admin only)"""
    if request.method == 'POST':
        hall_name = request.form.get('hall_name', '').strip()
        description = request.form.get('description', '').strip()
        capacity = request.form.get('capacity', type=int)
        price = request.form.get('price', type=float)
        working_from = request.form.get('working_from', '09:00')
        working_to = request.form.get('working_to', '22:00')
        
        if not all([hall_name, capacity, price]):
            flash('الرجاء ملء الحقول المطلوبة', 'error')
            return redirect(url_for('halls.add_hall'))

        hall = Hall(
            hall_name=hall_name,
            description=description,
            capacity=capacity,
            price=price,
            working_from=working_from,
            working_to=working_to,
            status='active'
        )
        
        db.session.add(hall)
        db.session.commit()
        
        # Log action
        log = StaffLog(
            user_id=current_user.id,
            action='add_hall',
            details=f'إضافة قاعة جديدة: {hall_name}'
        )
        db.session.add(log)
        db.session.commit()
        
        flash(f'تم إضافة القاعة "{hall_name}" بنجاح', 'success')
        return redirect(url_for('halls.manage_halls'))
    
    return render_template('halls/add.html')

@halls_bp.route('/<int:hall_id>/edit', methods=['GET', 'POST'])
@login_required
@admin_required
def edit_hall(hall_id):
    """Edit hall (Admin only)"""
    hall = Hall.query.get_or_404(hall_id)
    
    if request.method == 'POST':
        hall.hall_name = request.form.get('hall_name', '').strip()
        hall.description = request.form.get('description', '').strip()
        hall.capacity = request.form.get('capacity', type=int)
        hall.price = request.form.get('price', type=float)
        hall.working_from = request.form.get('working_from', '09:00')
        hall.working_to = request.form.get('working_to', '22:00')
        hall.status = request.form.get('status', 'active')

        db.session.commit()
        
        # Log action
        log = StaffLog(
            user_id=current_user.id,
            action='edit_hall',
            details=f'تعديل القاعة: {hall.hall_name}'
        )
        db.session.add(log)
        db.session.commit()
        
        flash(f'تم تحديث القاعة "{hall.hall_name}" بنجاح', 'success')
        return redirect(url_for('halls.manage_halls'))
    
    return render_template('halls/edit.html', hall=hall)

@halls_bp.route('/<int:hall_id>/delete', methods=['POST'])
@login_required
@admin_required
def delete_hall(hall_id):
    """Delete hall (Admin only)"""
    hall = Hall.query.get_or_404(hall_id)
    hall_name = hall.hall_name
    
    db.session.delete(hall)
    db.session.commit()
    
    # Log action
    log = StaffLog(
        user_id=current_user.id,
        action='delete_hall',
        details=f'حذف القاعة: {hall_name}'
    )
    db.session.add(log)
    db.session.commit()
    
    flash(f'تم حذف القاعة "{hall_name}" بنجاح', 'success')
    return redirect(url_for('halls.manage_halls'))


@halls_bp.route('/<int:hall_id>/calendar', methods=['GET'])
@login_required
def hall_calendar(hall_id):
    """Render a month calendar for a hall (partial HTML)"""
    hall = Hall.query.get_or_404(hall_id)
    try:
        year = int(request.args.get('year', datetime.now().year))
        month = int(request.args.get('month', datetime.now().month))
        # Validate month range
        if month < 1:
            month = 1
        elif month > 12:
            month = 12
        # Allow any year (past or future)
    except (ValueError, TypeError):
        year = datetime.now().year
        month = datetime.now().month

    # Arabic month names
    month_names_ar = [
        'يناير', 'فبراير', 'مارس', 'أبريل', 'مايو', 'يونيو',
        'يوليو', 'أغسطس', 'سبتمبر', 'أكتوبر', 'نوفمبر', 'ديسمبر'
    ]
    month_name = month_names_ar[month - 1]

    # Build weeks: list of weeks, each week is list of dicts {day, date, is_booked}
    first_weekday, days_in_month = monthrange(year, month)
    weeks = []
    week = []
    day_counter = 1

    # monthrange: first_weekday is 0=Monday ... adjust to Sunday-first for Arabic calendar header
    # We'll create calendar with 7 columns starting Sunday
    # Compute starting blanks: convert Python weekday (Mon=0) to our Sun-first index
    start_index = (first_weekday + 1) % 7

    for i in range(0, start_index):
        week.append({'day': 0})

    while day_counter <= days_in_month:
        dt = _date(year, month, day_counter)
        # Check if any booking exists on that date for this hall
        booked = Booking.query.filter_by(hall_id=hall.id, date=dt).filter(Booking.status != 'cancelled').count() > 0
        week.append({'day': day_counter, 'date': dt, 'is_booked': booked})
        if len(week) == 7:
            weeks.append(week)
            week = []
        day_counter += 1

    if week:
        # pad the remaining days
        while len(week) < 7:
            week.append({'day': 0})
        weeks.append(week)

    return render_template('halls/calendar.html', hall=hall, year=year, month=month, month_name=month_name, weeks=weeks)
