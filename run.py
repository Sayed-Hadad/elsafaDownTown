from app import create_app, db
from app.models import User, Hall, Booking, StaffLog
import os
from datetime import datetime, timedelta

app = create_app()

@app.shell_context_processor
def make_shell_context():
    return {
        'db': db,
        'User': User,
        'Hall': Hall,
        'Booking': Booking,
        'StaffLog': StaffLog
    }

def init_demo_data():
    """Initialize demo data for testing"""
    with app.app_context():
        # Check if data already exists
        if User.query.first():
            return
        
        # Create admin user
        admin = User(username='admin', role='admin')
        admin.set_password('admin123')
        db.session.add(admin)
        
        # Create staff user
        staff1 = User(username='staff1', role='staff')
        staff1.set_password('staff123')
        db.session.add(staff1)
        
        staff2 = User(username='staff2', role='staff')
        staff2.set_password('staff123')
        db.session.add(staff2)
        
        db.session.commit()
        
        # Create demo halls
        halls = [
            Hall(
                hall_name='قاعة الزفاف الكبرى',
                description='قاعة فاخرة مناسبة للحفلات والأعراس',
                capacity=500,
                price=5000,
                working_from='08:00',
                working_to='23:00',
                status='active'
            ),
            Hall(
                hall_name='قاعة المؤتمرات',
                description='قاعة حديثة مجهزة بأحدث التقنيات',
                capacity=200,
                price=2000,
                working_from='09:00',
                working_to='20:00',
                status='active'
            ),
            Hall(
                hall_name='قاعة الاجتماعات الصغرى',
                description='قاعة مريحة للاجتماعات والندوات',
                capacity=50,
                price=500,
                working_from='08:00',
                working_to='18:00',
                status='active'
            ),
            Hall(
                hall_name='قاعة الحفلات',
                description='قاعة متعددة الأغراض',
                capacity=300,
                price=3000,
                working_from='09:00',
                working_to='22:00',
                status='active'
            ),
        ]
        
        for hall in halls:
            # Add default addons to each demo hall
            hall.addons = [
                { 'name': 'Fire (صواريخ)', 'price': 1500, 'note': 'عرض ناري / صواريخ' },
                { 'name': 'كوشة', 'price': 800, 'note': '' },
                { 'name': 'ستاير', 'price': 600, 'note': '' }
            ]
            db.session.add(hall)
        
        db.session.commit()
        
        # Create demo bookings
        today = datetime.now().date()
        
        bookings = [
            Booking(
                hall_id=1,
                customer_name='أحمد محمد',
                phone='0501234567',
                phone_alt='0501234568',
                date=today + timedelta(days=7),
                start_time='18:00',
                end_time='22:00',
                deposit=1000,
                total_price=5000,
                notes='حفل زواج',
                created_by=staff1.id,
                status='pending'
            ),
            Booking(
                hall_id=2,
                customer_name='فاطمة علي',
                phone='0502345678',
                date=today + timedelta(days=3),
                start_time='10:00',
                end_time='14:00',
                deposit=500,
                total_price=2000,
                notes='مؤتمر شركة',
                created_by=staff1.id,
                status='approved'
            ),
            Booking(
                hall_id=3,
                customer_name='سلمان عبدالله',
                phone='0503456789',
                date=today + timedelta(days=1),
                start_time='09:00',
                end_time='11:00',
                deposit=200,
                total_price=500,
                notes='اجتماع إداري',
                created_by=staff2.id,
                status='completed'
            ),
            Booking(
                hall_id=4,
                customer_name='ليلى محمود',
                phone='0504567890',
                date=today + timedelta(days=14),
                start_time='19:00',
                end_time='23:00',
                deposit=800,
                total_price=3000,
                notes='حفل تخرج',
                created_by=staff2.id,
                status='pending'
            ),
        ]
        
        for booking in bookings:
            db.session.add(booking)
        
        db.session.commit()
        
        print("✓ Demo data initialized successfully!")

if __name__ == '__main__':
    import os
    # Initialize demo data only in development
    if os.environ.get('FLASK_ENV') != 'production':
        init_demo_data()
    
    # Run the app
    debug_mode = os.environ.get('FLASK_ENV') != 'production'
    port = int(os.environ.get('PORT', 5000))
    app.run(debug=debug_mode, host='0.0.0.0', port=port)
