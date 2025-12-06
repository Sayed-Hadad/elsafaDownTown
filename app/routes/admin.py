from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from app import db
from app.models import User, Booking, Hall, StaffLog, Addon
from app.utils import admin_required
from datetime import datetime, timedelta
from sqlalchemy import func
from flask import current_app

admin_bp = Blueprint('admin', __name__, url_prefix='/admin')

@admin_bp.route('/dashboard', methods=['GET'])
@login_required
@admin_required
def dashboard():
    """Admin dashboard with statistics"""
    today = datetime.now().date()
    
    # Statistics
    total_bookings_today = Booking.query.filter(
        Booking.date == today,
        Booking.status != 'cancelled'
    ).count()
    
    total_upcoming_bookings = Booking.query.filter(
        Booking.date >= today,
        Booking.status != 'cancelled'
    ).count()
    
    total_deposits = db.session.query(func.sum(Booking.deposit)).filter(
        Booking.status != 'cancelled'
    ).scalar() or 0
    
    # Get halls occupancy
    halls = Hall.query.all()
    
    # Latest staff logs
    latest_logs = StaffLog.query.order_by(StaffLog.timestamp.desc()).limit(10).all()
    
    # Get pending bookings
    pending_bookings = Booking.query.filter_by(status='pending').order_by(Booking.created_at.desc()).limit(5).all()
    
    return render_template('admin/dashboard.html',
                         total_bookings_today=total_bookings_today,
                         total_upcoming_bookings=total_upcoming_bookings,
                         total_deposits=total_deposits,
                         halls=halls,
                         latest_logs=latest_logs,
                         pending_bookings=pending_bookings)


def seed_addons_if_empty():
    if Addon.query.count() == 0:
        defaults = current_app.config.get('AVAILABLE_ADDONS', [])
        for item in defaults:
            addon = Addon(
                code=item.get('id'),
                name=item.get('name'),
                description=item.get('desc'),
                icon=item.get('icon'),
                price=item.get('price', 0),
                active=True
            )
            db.session.add(addon)
        db.session.commit()


@admin_bp.route('/addons', methods=['GET', 'POST'])
@login_required
@admin_required
def addons():
    """Manage add-ons catalog"""
    seed_addons_if_empty()

    if request.method == 'POST':
        code = request.form.get('code', '').strip()
        name = request.form.get('name', '').strip()
        description = request.form.get('description', '').strip()
        icon = request.form.get('icon', '').strip()
        price = request.form.get('price', type=float, default=0)

        if not code or not name:
            flash('الكود والاسم مطلوبان', 'error')
            return redirect(url_for('admin.addons'))

        if Addon.query.filter_by(code=code).first():
            flash('الكود مستخدم بالفعل', 'error')
            return redirect(url_for('admin.addons'))

        addon = Addon(code=code, name=name, description=description, icon=icon, price=price, active=True)
        db.session.add(addon)
        db.session.commit()
        flash('تم إضافة الإضافة بنجاح', 'success')
        return redirect(url_for('admin.addons'))

    addons = Addon.query.order_by(Addon.active.desc(), Addon.name.asc()).all()
    return render_template('admin/addons.html', addons=addons)


@admin_bp.route('/addons/<int:addon_id>', methods=['POST'])
@login_required
@admin_required
def update_addon(addon_id):
    """Update an existing addon"""
    addon = Addon.query.get_or_404(addon_id)

    addon.name = request.form.get('name', addon.name).strip()
    addon.description = request.form.get('description', '').strip()
    addon.icon = request.form.get('icon', '').strip()
    addon.price = request.form.get('price', type=float, default=addon.price)
    addon.active = True if request.form.get('active') else False

    db.session.commit()
    flash('تم تحديث الإضافة', 'success')
    return redirect(url_for('admin.addons'))

@admin_bp.route('/bookings', methods=['GET'])
@login_required
@admin_required
def view_all_bookings():
    """View all bookings (Admin only)"""
    page = request.args.get('page', 1, type=int)
    search = request.args.get('search', '').strip()
    hall_id = request.args.get('hall_id', type=int)
    status = request.args.get('status', '').strip()
    
    query = Booking.query
    
    if search:
        # Search by customer name or phone number
        from sqlalchemy import or_
        query = query.filter(
            or_(
                Booking.customer_name.ilike(f'%{search}%'),
                Booking.phone.ilike(f'%{search}%'),
                Booking.phone_alt.ilike(f'%{search}%')
            )
        )
    
    if hall_id:
        query = query.filter_by(hall_id=hall_id)
    
    if status:
        query = query.filter_by(status=status)
    
    bookings = query.order_by(Booking.date.desc(), Booking.start_time.desc()).paginate(page=page, per_page=15)
    halls = Hall.query.all()
    
    return render_template('admin/bookings.html',
                         bookings=bookings,
                         halls=halls,
                         search=search,
                         hall_id=hall_id,
                         status=status)

@admin_bp.route('/bookings/<int:booking_id>/approve', methods=['POST'])
@login_required
@admin_required
def approve_booking(booking_id):
    """Approve a booking"""
    booking = Booking.query.get_or_404(booking_id)
    booking.status = 'approved'
    db.session.commit()
    
    log = StaffLog(
        user_id=current_user.id,
        action='approve_booking',
        details=f'تصريح الحجز: {booking.customer_name}'
    )
    db.session.add(log)
    db.session.commit()
    
    flash('تم تصريح الحجز بنجاح', 'success')
    return redirect(request.referrer or url_for('admin.view_all_bookings'))

@admin_bp.route('/bookings/<int:booking_id>/reject', methods=['POST'])
@login_required
@admin_required
def reject_booking(booking_id):
    """Reject a booking"""
    booking = Booking.query.get_or_404(booking_id)
    booking.status = 'cancelled'
    db.session.commit()
    
    log = StaffLog(
        user_id=current_user.id,
        action='reject_booking',
        details=f'رفض الحجز: {booking.customer_name}'
    )
    db.session.add(log)
    db.session.commit()
    
    flash('تم رفض الحجز', 'success')
    return redirect(request.referrer or url_for('admin.view_all_bookings'))

@admin_bp.route('/staff', methods=['GET'])
@login_required
@admin_required
def manage_staff():
    """Manage staff accounts"""
    page = request.args.get('page', 1, type=int)
    staff = User.query.paginate(page=page, per_page=10)
    return render_template('admin/staff.html', staff=staff)

@admin_bp.route('/staff/add', methods=['GET', 'POST'])
@login_required
@admin_required
def add_staff():
    """Add new staff member"""
    if request.method == 'POST':
        username = request.form.get('username', '').strip()
        password = request.form.get('password', '')
        role = request.form.get('role', 'staff')
        
        if not username or not password:
            flash('الرجاء ملء جميع الحقول', 'error')
            return redirect(url_for('admin.add_staff'))
        
        if User.query.filter_by(username=username).first():
            flash('اسم المستخدم موجود بالفعل', 'error')
            return redirect(url_for('admin.add_staff'))
        
        user = User(username=username, role=role)
        user.set_password(password)
        
        db.session.add(user)
        db.session.commit()
        
        log = StaffLog(
            user_id=current_user.id,
            action='add_staff',
            details=f'إضافة موظف جديد: {username}'
        )
        db.session.add(log)
        db.session.commit()
        
        flash(f'تم إضافة الموظف "{username}" بنجاح', 'success')
        return redirect(url_for('admin.manage_staff'))
    
    return render_template('admin/add_staff.html')

@admin_bp.route('/staff/<int:user_id>/edit', methods=['GET', 'POST'])
@login_required
@admin_required
def edit_staff(user_id):
    """Edit staff member"""
    user = User.query.get_or_404(user_id)
    
    if request.method == 'POST':
        user.role = request.form.get('role', 'staff')
        new_password = request.form.get('password', '').strip()
        
        if new_password:
            user.set_password(new_password)
        
        db.session.commit()
        
        log = StaffLog(
            user_id=current_user.id,
            action='edit_staff',
            details=f'تعديل بيانات الموظف: {user.username}'
        )
        db.session.add(log)
        db.session.commit()
        
        flash(f'تم تحديث بيانات الموظف بنجاح', 'success')
        return redirect(url_for('admin.manage_staff'))
    
    return render_template('admin/edit_staff.html', user=user)

@admin_bp.route('/staff/<int:user_id>/delete', methods=['POST'])
@login_required
@admin_required
def delete_staff(user_id):
    """Delete staff member"""
    if user_id == current_user.id:
        flash('لا يمكنك حذف حسابك الخاص', 'error')
        return redirect(url_for('admin.manage_staff'))
    
    user = User.query.get_or_404(user_id)
    username = user.username
    
    db.session.delete(user)
    db.session.commit()
    
    log = StaffLog(
        user_id=current_user.id,
        action='delete_staff',
        details=f'حذف الموظف: {username}'
    )
    db.session.add(log)
    db.session.commit()
    
    flash(f'تم حذف الموظف بنجاح', 'success')
    return redirect(url_for('admin.manage_staff'))

@admin_bp.route('/activity-logs', methods=['GET'])
@login_required
@admin_required
def activity_logs():
    """View activity logs"""
    page = request.args.get('page', 1, type=int)
    user_id = request.args.get('user_id', type=int)
    action = request.args.get('action', '').strip()
    
    query = StaffLog.query
    
    if user_id:
        query = query.filter_by(user_id=user_id)
    
    if action:
        query = query.filter_by(action=action)
    
    logs = query.order_by(StaffLog.timestamp.desc()).paginate(page=page, per_page=20)
    users = User.query.all()
    
    return render_template('admin/activity_logs.html',
                         logs=logs,
                         users=users,
                         user_id=user_id,
                         action=action)

@admin_bp.route('/calendar', methods=['GET'])
@login_required
@admin_required
def calendar_view():
    """Full calendar view of all halls"""
    year = request.args.get('year', type=int)
    month = request.args.get('month', type=int)
    
    if not year or not month:
        now = datetime.now()
        year, month = now.year, now.month
    
    halls = Hall.query.filter_by(status='active').all()
    
    return render_template('admin/calendar.html',
                         year=year,
                         month=month,
                         halls=halls)
