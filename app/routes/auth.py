from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from flask_login import login_user, logout_user, login_required, current_user
from app import db
from app.models import User, StaffLog
from datetime import datetime

auth_bp = Blueprint('auth', __name__, url_prefix='/auth')

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('dashboard.index'))
    
    if request.method == 'POST':
        username = request.form.get('username', '').strip()
        password = request.form.get('password', '')
        remember_me = request.form.get('remember_me')
        
        if not username or not password:
            flash('الرجاء ملء جميع الحقول', 'error')
            return redirect(url_for('auth.login'))
        
        user = User.query.filter_by(username=username).first()
        
        if user and user.check_password(password) and user.is_active:
            login_user(user, remember=bool(remember_me))
            session.permanent = bool(remember_me)
            
            # Log login action
            log = StaffLog(
                user_id=user.id,
                action='login',
                details=f'تسجيل دخول من {request.remote_addr}'
            )
            db.session.add(log)
            db.session.commit()
            
            flash(f'أهلاً وسهلاً {user.username}!', 'success')
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('dashboard.index'))
        else:
            flash('اسم المستخدم أو كلمة المرور غير صحيحة', 'error')
    
    return render_template('auth/login.html')


@auth_bp.route('/logout', methods=['POST'])
@login_required
def logout():
    # Log logout action
    log = StaffLog(
        user_id=current_user.id,
        action='logout',
        details=f'تسجيل خروج من {request.remote_addr}'
    )
    db.session.add(log)
    db.session.commit()
    
    logout_user()
    flash('تم تسجيل الخروج بنجاح', 'success')
    return redirect(url_for('auth.login'))


@auth_bp.route('/unauthorized')
def unauthorized():
    flash('ليس لديك صلاحيات للوصول لهذه الصفحة', 'error')
    return redirect(url_for('dashboard.index'))
