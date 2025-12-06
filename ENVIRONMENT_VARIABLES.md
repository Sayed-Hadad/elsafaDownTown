# 🔐 Environment Variables for Deployment

This document lists all environment variables required for deploying the Safa Downtown Halls application.

## 📋 Required Environment Variables

### 1. **SECRET_KEY** ⚠️ REQUIRED
- **Description**: Secret key for Flask session encryption and security
- **Type**: String (random secret)
- **Example**: `your-super-secret-key-here-min-32-chars`
- **How to generate**: 
  ```python
  import secrets
  print(secrets.token_hex(32))
  ```
  Or use: `python -c "import secrets; print(secrets.token_hex(32))"`
- **Default**: `elsafa-halls-secret-key-2025` (⚠️ **CHANGE THIS IN PRODUCTION!**)

### 2. **DATABASE_URL** ⚠️ REQUIRED (for production)
- **Description**: Database connection string
- **Type**: String (PostgreSQL connection URI)
- **Format**: `postgresql://username:password@host:port/database`
- **Example**: `postgresql://user:pass@localhost:5432/elsafa_halls`
- **Note**: 
  - For Render.com: Automatically provided when you connect a PostgreSQL database
  - For other platforms: You need to create a PostgreSQL database and get the connection string
- **Default**: Uses SQLite (`sqlite:///elsafa_halls.db`) if not set (⚠️ **Not recommended for production**)

---

## 🔧 Optional Environment Variables

### 3. **FLASK_ENV**
- **Description**: Flask environment mode
- **Type**: String
- **Values**: `development` | `production`
- **Default**: `development` (if not set)
- **Recommended**: Set to `production` for deployment

### 4. **PORT**
- **Description**: Port number for the application to run on
- **Type**: Integer
- **Default**: `5000`
- **Note**: Most deployment platforms (Render, Heroku, etc.) set this automatically via `$PORT`

### 5. **SESSION_COOKIE_SECURE**
- **Description**: Enable secure cookies (HTTPS only)
- **Type**: Boolean/String
- **Values**: `true` | `false`
- **Default**: `false` (set to `true` in production with HTTPS)
- **Note**: Automatically set in `render.yaml` for Render deployments

### 6. **SESSION_COOKIE_HTTPONLY**
- **Description**: Prevent JavaScript access to cookies
- **Type**: Boolean/String
- **Values**: `true` | `false`
- **Default**: `true`
- **Note**: Security best practice

### 7. **SESSION_COOKIE_SAMESITE**
- **Description**: CSRF protection for cookies
- **Type**: String
- **Values**: `Lax` | `Strict` | `None`
- **Default**: `Lax`

---

## 🚀 Platform-Specific Instructions

### Render.com
If using `render.yaml`, these are automatically configured:
- ✅ `SECRET_KEY` - Auto-generated
- ✅ `DATABASE_URL` - Auto-linked from PostgreSQL database
- ✅ `FLASK_ENV=production`
- ✅ `SESSION_COOKIE_SECURE=true`

**Manual setup on Render:**
1. Go to your Web Service → Environment
2. Add these variables:
   - `SECRET_KEY` (click "Generate" or paste your own)
   - `DATABASE_URL` (from your PostgreSQL database)
   - `FLASK_ENV=production`

### Heroku
```bash
heroku config:set SECRET_KEY=your-secret-key-here
heroku config:set DATABASE_URL=postgresql://...
heroku config:set FLASK_ENV=production
```

### Vercel / Netlify / Other Platforms
Add these in your platform's environment variables section:
- `SECRET_KEY` (required)
- `DATABASE_URL` (required - you'll need to set up PostgreSQL separately)
- `FLASK_ENV=production` (recommended)
- `PORT` (usually set automatically by platform)

---

## 🔒 Security Checklist

Before deploying, ensure:

- [ ] `SECRET_KEY` is set to a strong, random value (not the default)
- [ ] `DATABASE_URL` points to a production PostgreSQL database (not SQLite)
- [ ] `FLASK_ENV=production` is set
- [ ] `SESSION_COOKIE_SECURE=true` (if using HTTPS)
- [ ] Never commit `.env` files or secrets to Git
- [ ] Use your platform's secure environment variable storage

---

## 📝 Example .env File (for local development)

Create a `.env` file in the project root (⚠️ **DO NOT commit this to Git!**):

```env
SECRET_KEY=your-local-development-secret-key-here
DATABASE_URL=sqlite:///elsafa_halls.db
FLASK_ENV=development
PORT=5000
```

For production, use your platform's environment variable settings instead of a `.env` file.

---

## 🆘 Troubleshooting

### "SECRET_KEY not set" warning
- Set `SECRET_KEY` environment variable in your deployment platform

### Database connection errors
- Verify `DATABASE_URL` is correct
- Ensure PostgreSQL database is running and accessible
- Check firewall/network settings if using external database

### Session/cookie issues
- Set `SESSION_COOKIE_SECURE=true` only if using HTTPS
- Verify `SESSION_COOKIE_HTTPONLY=true` for security

---

## 📚 Additional Resources

- See `RENDER_DEPLOYMENT.md` for Render-specific instructions
- See `config.py` for all configuration options
- Flask Environment Variables: https://flask.palletsprojects.com/en/latest/config/

