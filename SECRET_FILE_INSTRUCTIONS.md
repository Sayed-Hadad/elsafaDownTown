# 📁 Secret Files for Render.com

## How to Use Secret Files

Instead of adding environment variables one by one, you can upload a `.env` file to Render's "Secret Files" section.

---

## 📝 Steps:

### 1. Generate SECRET_KEY

Run this command to generate a secure secret key:
```bash
python -c "import secrets; print(secrets.token_hex(32))"
```

Copy the output.

### 2. Get DATABASE_URL

1. First, create a PostgreSQL database in Render:
   - Go to Render Dashboard
   - Click "New" → "PostgreSQL"
   - Create the database
   - After creation, go to the database page
   - Copy the "Internal Database URL" or "Connection String"

### 3. Edit the .env File

1. Open `render.env` file in this project
2. Replace `CHANGE_THIS_TO_YOUR_GENERATED_SECRET_KEY` with your generated SECRET_KEY
3. Replace `CHANGE_THIS_TO_YOUR_DATABASE_URL` with your PostgreSQL connection string

### 4. Upload to Render

1. In Render deployment form, scroll to "Secret Files" section
2. Click "Add Secret File"
3. **File Name**: `.env`
4. **File Contents**: Copy and paste the contents of your edited `render.env` file
5. Click "Save"

---

## ✅ What This Does:

Render will:
- Make the `.env` file available at `/etc/secrets/.env` during builds
- Make it available at runtime in your app's root directory
- Automatically load environment variables from it

---

## 🔒 Security Notes:

- ⚠️ **NEVER commit `.env` files to Git**
- ✅ The `render.env` file is a template - edit it before uploading
- ✅ Render encrypts secret files at rest
- ✅ Only accessible to your service

---

## 📋 Quick Checklist:

- [ ] Generated SECRET_KEY
- [ ] Created PostgreSQL database in Render
- [ ] Copied DATABASE_URL from database
- [ ] Edited `render.env` with real values
- [ ] Uploaded `.env` to Render Secret Files section

---

## 🎯 Alternative: Use Environment Variables Instead

If you prefer not to use Secret Files, you can add each variable individually in the "Environment Variables" section. Both methods work the same way!

---

## 📄 File Location:

The file `render.env` in your project root is the template. Edit it and upload to Render.

