from flask import Blueprint, render_template, jsonify, request
from flask_login import login_required, current_user
from app import db
from app.models import Booking, Hall
from datetime import datetime, timedelta
from calendar import monthrange
import json

api_bp = Blueprint('api', __name__, url_prefix='/api')

def get_calendar_days(year, month):
    """Generate calendar days for a given month"""
    today = datetime.now().date()
    days = []
    
    # Get first day of month and number of days
    first_day_weekday, num_days = monthrange(year, month)
    
    # Add empty cells for days before month starts
    for _ in range(first_day_weekday):
        days.append(None)
    
    # Add all days of the month
    for day in range(1, num_days + 1):
        date = datetime(year, month, day).date()
        is_past = date < today
        is_today = date == today
        
        days.append({
            'date': date.isoformat(),
            'day': day,
            'is_past': is_past,
            'is_today': is_today
        })
    
    return days

@api_bp.route('/calendar', methods=['GET'])
@login_required
def get_calendar():
    """Get calendar for a specific month"""
    month_str = request.args.get('month', '')  # Format: YYYY-MM
    
    if not month_str:
        now = datetime.now()
        year, month = now.year, now.month
    else:
        try:
            date = datetime.strptime(month_str, '%Y-%m')
            year, month = date.year, date.month
        except ValueError:
            return jsonify({'error': 'Invalid month format'}), 400
    
    # Check if trying to access past months
    today = datetime.now().date()
    first_of_month = datetime(year, month, 1).date()
    
    if first_of_month < today.replace(day=1):
        # Can only view current month and future
        now = datetime.now()
        year, month = now.year, now.month
    
    days = get_calendar_days(year, month)
    
    return jsonify({
        'year': year,
        'month': month,
        'month_name': datetime(year, month, 1).strftime('%B'),
        'days': days
    })

@api_bp.route('/availability', methods=['GET'])
@login_required
def get_availability():
    """Get available time slots for a hall on a specific date"""
    hall_id = request.args.get('hall_id', type=int)
    date_str = request.args.get('date', '')  # Format: YYYY-MM-DD
    
    if not hall_id or not date_str:
        return jsonify({'error': 'Missing parameters'}), 400
    
    hall = Hall.query.get(hall_id)
    if not hall:
        return jsonify({'error': 'Hall not found'}), 404
    
    try:
        date = datetime.strptime(date_str, '%Y-%m-%d').date()
    except ValueError:
        return jsonify({'error': 'Invalid date format'}), 400
    
    # Check if date is in the past
    if date < datetime.now().date():
        return jsonify({'error': 'Cannot book past dates'}), 400
    
    # Get hall working hours
    working_from = hall.working_from  # HH:MM
    working_to = hall.working_to      # HH:MM
    
    # Get all bookings for this hall on this date (excluding cancelled)
    bookings = Booking.query.filter(
        Booking.hall_id == hall_id,
        Booking.date == date,
        Booking.status != 'cancelled'
    ).all()

    # Prepare booked ranges for UI popups
    booked_ranges = [
        {
            'start_time': b.start_time,
            'end_time': b.end_time,
            'customer_name': b.customer_name
        }
        for b in bookings
    ]
    
    # Generate time slots (30-minute intervals)
    time_slots = []
    from_hour, from_min = map(int, working_from.split(':'))
    to_hour, to_min = map(int, working_to.split(':'))
    
    current_time = datetime(2000, 1, 1, from_hour, from_min)
    end_time = datetime(2000, 1, 1, to_hour, to_min)
    
    full_day_booked = False

    # If any booking covers the full working window, mark day as fully booked
    for b in bookings:
        if b.start_time <= working_from and b.end_time >= working_to:
            full_day_booked = True
            break

    while current_time < end_time:
        slot_time = current_time.strftime('%H:%M')
        slot_end = (current_time + timedelta(minutes=30)).strftime('%H:%M')
        
        # Check if this slot is booked
        is_booked = full_day_booked or any(
            booking.start_time <= slot_time < booking.end_time
            for booking in bookings
        )
        
        time_slots.append({
            'time': slot_time,
            'end_time': slot_end,
            'is_booked': is_booked
        })
        
        current_time += timedelta(minutes=30)
    
    return jsonify({
        'date': date_str,
        'hall_id': hall_id,
        'hall_name': hall.hall_name,
        'capacity': hall.capacity,
        'price': hall.price,
        'working_from': working_from,
        'working_to': working_to,
        'time_slots': time_slots,
        'booked_ranges': booked_ranges,
        'full_day_booked': full_day_booked
    })

@api_bp.route('/bookings', methods=['GET'])
@login_required
def get_bookings():
    """Get bookings for a specific hall and month"""
    hall_id = request.args.get('hall_id', type=int)
    year = request.args.get('year', type=int)
    month = request.args.get('month', type=int)
    
    if not hall_id or not year or not month:
        return jsonify({'error': 'Missing parameters'}), 400
    
    # Get all bookings for this hall in this month
    from datetime import date as _date
    start_date = _date(year, month, 1)
    
    # Calculate last day of month
    from calendar import monthrange
    _, last_day = monthrange(year, month)
    end_date = _date(year, month, last_day)
    
    bookings = Booking.query.filter(
        Booking.hall_id == hall_id,
        Booking.date >= start_date,
        Booking.date <= end_date,
        Booking.status != 'cancelled'
    ).all()
    
    # Convert to JSON format
    bookings_list = []
    for booking in bookings:
        bookings_list.append({
            'id': booking.id,
            'customer_name': booking.customer_name,
            'phone': booking.phone,
            'date': booking.date.isoformat(),
            'start_time': booking.start_time,
            'end_time': booking.end_time,
            'status': booking.status,
            'total_price': booking.total_price,
            'deposit': booking.deposit
        })
    
    return jsonify({
        'hall_id': hall_id,
        'year': year,
        'month': month,
        'bookings': bookings_list
    })