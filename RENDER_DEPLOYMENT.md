# 🚀 دليل النشر على Render.com

## 📋 المتطلبات

1. حساب على [Render.com](https://render.com)
2. مستودع Git (GitHub, GitLab, أو Bitbucket)
3. التطبيق يجب أن يكون في المستودع

---

## 🔧 الإعدادات

### 1. إعداد قاعدة البيانات

التطبيق يستخدم PostgreSQL على Render. قاعدة البيانات ستُنشأ تلقائياً من ملف `render.yaml`.

### 2. متغيرات البيئة

سيتم إعدادها تلقائياً من `render.yaml`:
- `SECRET_KEY` - سيتم توليده تلقائياً
- `DATABASE_URL` - سيتم ربطه بقاعدة البيانات تلقائياً
- `FLASK_ENV=production`
- `SESSION_COOKIE_SECURE=true`

### 3. متغيرات إضافية (اختيارية)

يمكن إضافة متغيرات إضافية من لوحة تحكم Render:
- `TIMEZONE` - المنطقة الزمنية (افتراضي: Asia/Riyadh)
- `LANGUAGE` - اللغة (افتراضي: ar)

---

## 📝 خطوات النشر

### الطريقة الأولى: استخدام render.yaml (موصى بها)

1. **ادفع الكود إلى Git:**
   ```bash
   git add .
   git commit -m "Add render.yaml for deployment"
   git push origin main
   ```

2. **في Render Dashboard:**
   - اذهب إلى [Render Dashboard](https://dashboard.render.com)
   - اضغط على "New" → "Blueprint"
   - اختر المستودع الخاص بك
   - Render سيكتشف `render.yaml` تلقائياً
   - اضغط "Apply"

3. **انتظر حتى يكتمل البناء:**
   - Render سيبني التطبيق تلقائياً
   - ستنشأ قاعدة البيانات تلقائياً
   - سيتم ربط قاعدة البيانات بالتطبيق

### الطريقة الثانية: النشر اليدوي

1. **إنشاء قاعدة البيانات:**
   - اذهب إلى Render Dashboard
   - اضغط "New" → "PostgreSQL"
   - اختر الخطة (Free للبداية)
   - احفظ معلومات الاتصال

2. **إنشاء Web Service:**
   - اضغط "New" → "Web Service"
   - اختر المستودع
   - الإعدادات:
     - **Name:** safa-downtown-halls
     - **Environment:** Python 3
     - **Build Command:** `pip install -r requirements.txt`
     - **Start Command:** `gunicorn run:app --bind 0.0.0.0:$PORT`
   - أضف متغيرات البيئة:
     - `SECRET_KEY` (Generate)
     - `DATABASE_URL` (من قاعدة البيانات)
     - `FLASK_ENV=production`

3. **ربط قاعدة البيانات:**
   - في صفحة Web Service
   - اضغط "Connect" بجانب قاعدة البيانات

---

## 🔄 تهيئة قاعدة البيانات

بعد النشر الأول، يجب تهيئة قاعدة البيانات:

### الطريقة الأولى: من Render Shell

1. اذهب إلى Web Service
2. اضغط على "Shell"
3. نفذ:
   ```bash
   python -c "from app import create_app, db; app = create_app(); app.app_context().push(); db.create_all()"
   ```

### الطريقة الثانية: من الكود

يمكن إضافة دالة تهيئة في `run.py`:

```python
@app.before_first_request
def create_tables():
    db.create_all()
```

---

## 🎯 إنشاء المستخدم الأول

بعد تهيئة قاعدة البيانات، يمكنك إنشاء المستخدم الأول:

### من Render Shell:

```python
from app import create_app, db
from app.models import User

app = create_app()
with app.app_context():
    admin = User(username='admin', role='admin')
    admin.set_password('admin123')
    db.session.add(admin)
    db.session.commit()
    print("Admin user created!")
```

---

## 🔒 الأمان

### 1. HTTPS
Render يوفر HTTPS تلقائياً لجميع الخدمات.

### 2. SECRET_KEY
يتم توليده تلقائياً من Render.

### 3. قاعدة البيانات
PostgreSQL محمية ومشفرة.

---

## 📊 المراقبة والـ Logs

- **Logs:** متاحة في صفحة Web Service
- **Metrics:** متاحة في قسم Metrics
- **Health Checks:** يتم فحصها تلقائياً

---

## 🔄 التحديثات التلقائية

عند تفعيل `autoDeploy: true` في `render.yaml`:
- أي push إلى الفرع الرئيسي سيؤدي إلى إعادة النشر تلقائياً

---

## 🐛 استكشاف الأخطاء

### المشكلة: التطبيق لا يعمل
- تحقق من Logs في Render Dashboard
- تأكد من أن `DATABASE_URL` صحيح
- تأكد من أن `SECRET_KEY` موجود

### المشكلة: قاعدة البيانات غير متصلة
- تحقق من أن قاعدة البيانات نشطة
- تحقق من `DATABASE_URL` في متغيرات البيئة
- تأكد من أن قاعدة البيانات في نفس المنطقة

### المشكلة: خطأ في البناء
- تحقق من `requirements.txt`
- تأكد من أن جميع المكتبات متوافقة
- تحقق من Logs في قسم Build

---

## 💰 الخطط والأسعار

### Free Plan:
- Web Service: 750 ساعة/شهر
- PostgreSQL: 90 يوم تجريبي
- مناسب للاختبار والتطوير

### Starter Plan ($7/شهر):
- Web Service: غير محدود
- PostgreSQL: 1GB
- مناسب للإنتاج الصغير

### Standard Plan ($25/شهر):
- Web Service: غير محدود
- PostgreSQL: 10GB
- مناسب للإنتاج المتوسط

---

## 📝 ملاحظات مهمة

1. **SQLite → PostgreSQL:**
   - التطبيق يستخدم SQLite محلياً
   - على Render، استخدم PostgreSQL
   - `DATABASE_URL` سيتغير تلقائياً

2. **الملفات الثابتة:**
   - الملفات المرفوعة ستُحذف عند إعادة النشر
   - استخدم خدمة تخزين خارجية (S3) للملفات

3. **النسخ الاحتياطي:**
   - Render يوفر نسخ احتياطي تلقائي لقاعدة البيانات
   - يمكنك تنزيل النسخ الاحتياطي من Dashboard

---

## 🔗 روابط مفيدة

- [Render Documentation](https://render.com/docs)
- [Flask on Render](https://render.com/docs/deploy-flask)
- [PostgreSQL on Render](https://render.com/docs/databases)

---

**آخر تحديث:** 2025

