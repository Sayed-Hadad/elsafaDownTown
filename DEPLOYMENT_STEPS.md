# 🚀 Step-by-Step Deployment Guide

## Option 1: Deploy to Render.com (Recommended - Easiest)

Your project already has `render.yaml` configured! Here's what to do:

### Step 1: Generate SECRET_KEY (Optional - Render can auto-generate)
```bash
python -c "import secrets; print(secrets.token_hex(32))"
```
Copy the output - you'll use it if you want to set it manually.

### Step 2: Push to GitHub/GitLab/Bitbucket
```bash
git add .
git commit -m "Ready for deployment"
git push origin main
```

### Step 3: Deploy on Render.com
1. Go to [https://dashboard.render.com](https://dashboard.render.com)
2. Click **"New"** → **"Blueprint"**
3. Connect your Git repository
4. Render will automatically detect `render.yaml`
5. Click **"Apply"**

### Step 4: Wait for Deployment
- Render will automatically:
  - ✅ Create PostgreSQL database
  - ✅ Generate SECRET_KEY
  - ✅ Link DATABASE_URL
  - ✅ Set all environment variables
  - ✅ Build and deploy your app

### Step 5: Initialize Database (After first deployment)
1. Go to your Web Service on Render
2. Click **"Shell"** tab
3. Run:
```bash
python -c "from app import create_app, db; app = create_app(); app.app_context().push(); db.create_all()"
```

### Step 6: Create Admin User
In the same Shell, run:
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

**That's it!** Your app should be live. 🎉

---

## Option 2: Deploy to Other Platforms (Vercel, Heroku, etc.)

### Step 1: Generate SECRET_KEY
```bash
python -c "import secrets; print(secrets.token_hex(32))"
```
Copy the output.

### Step 2: Set Up PostgreSQL Database
- **Heroku**: Add Heroku Postgres addon
- **Railway**: Create PostgreSQL service
- **DigitalOcean**: Create managed database
- **AWS**: Set up RDS PostgreSQL

Get your database connection string (format: `postgresql://user:pass@host:port/db`)

### Step 3: Add Environment Variables
In your platform's dashboard, add these:

| Variable Name | Value | Notes |
|--------------|-------|-------|
| `SECRET_KEY` | [Paste the generated key] | Required |
| `DATABASE_URL` | [Your PostgreSQL connection string] | Required |
| `FLASK_ENV` | `production` | Recommended |
| `PORT` | (Usually auto-set) | Platform sets this |
| `SESSION_COOKIE_SECURE` | `true` | If using HTTPS |

### Step 4: Deploy
Follow your platform's deployment instructions.

---

## Option 3: Manual Setup (If render.yaml doesn't work)

### On Render.com Dashboard:

1. **Create PostgreSQL Database:**
   - Click "New" → "PostgreSQL"
   - Name: `safa-halls-db`
   - Plan: Free (or your choice)
   - Region: Choose closest to you
   - Click "Create"

2. **Create Web Service:**
   - Click "New" → "Web Service"
   - Connect your Git repository
   - Settings:
     - **Name**: `safa-downtown-halls`
     - **Environment**: `Python 3`
     - **Build Command**: `pip install -r requirements.txt`
     - **Start Command**: `gunicorn run:app --bind 0.0.0.0:$PORT --workers 2 --timeout 120`

3. **Add Environment Variables:**
   Click "Environment" tab and add:
   
   | Key | Value |
   |-----|-------|
   | `SECRET_KEY` | [Click "Generate" or paste your generated key] |
   | `DATABASE_URL` | [Copy from PostgreSQL database → "Internal Database URL"] |
   | `FLASK_ENV` | `production` |
   | `FLASK_APP` | `run.py` |
   | `PYTHON_VERSION` | `3.11.0` |
   | `SESSION_COOKIE_SECURE` | `true` |
   | `SESSION_COOKIE_HTTPONLY` | `true` |
   | `SESSION_COOKIE_SAMESITE` | `Lax` |

4. **Link Database:**
   - In Web Service page
   - Scroll to "Connections"
   - Click "Connect" next to your PostgreSQL database

5. **Deploy:**
   - Click "Save Changes"
   - Wait for build to complete

---

## ✅ Quick Checklist

Before deploying, make sure:
- [ ] Code is pushed to Git repository
- [ ] `requirements.txt` is up to date
- [ ] `render.yaml` exists (for Render) OR you know your platform
- [ ] You have a PostgreSQL database ready (or Render will create it)
- [ ] You've generated a SECRET_KEY

After deployment:
- [ ] Database is initialized (run `db.create_all()`)
- [ ] Admin user is created
- [ ] App is accessible via URL
- [ ] You can log in with admin credentials

---

## 🆘 Need Help?

- **Render.com**: See `RENDER_DEPLOYMENT.md`
- **Environment Variables**: See `ENVIRONMENT_VARIABLES.md`
- **Quick Reference**: See `DEPLOYMENT_ENV_VARS.txt`

---

## 🎯 What Platform Are You Using?

Tell me which platform you're deploying to, and I can give you specific instructions!

