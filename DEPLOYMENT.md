# Deployment Guide: Flask Auth App to Render

Complete step-by-step guide to deploy your Flask application to Render.com (modern alternative to Heroku).

## Prerequisites

- GitHub account
- Render account (free at render.com)
- Local Flask app tested and working
- All code pushed to GitHub

---

## Step 1: Prepare Your Application

### 1.1 Update requirements.txt
Ensure `requirements.txt` is in your root directory:
```
Flask==3.0.0
Flask-SQLAlchemy==3.1.1
Flask-Login==0.6.3
Flask-Migrate==4.0.5
Werkzeug==3.0.1
SQLAlchemy==2.0.23
Gunicorn==21.2.0
python-dotenv==1.0.0
Click==8.1.7
```

### 1.2 Create Procfile
File: `Procfile` (no extension, in root directory)
```
web: gunicorn app:app
```

### 1.3 Create runtime.txt
File: `runtime.txt` (in root directory)
```
python-3.11.7
```

### 1.4 Create build.sh (optional but recommended)
File: `build.sh`
```bash
#!/bin/bash
set -o errexit

pip install -r requirements.txt

# Initialize database
python -c "from app import app, db; app.app_context().push(); db.create_all()"

echo "Build completed successfully!"
```

### 1.5 Create .env.example
File: `.env.example` (template for environment variables)
```
FLASK_ENV=development
SECRET_KEY=your-secret-key-here
PORT=5000
DATABASE_URL=sqlite:///flaskapp.db
SESSION_COOKIE_SECURE=False
```

### 1.6 Update .gitignore
Ensure `.gitignore` includes:
```
.env
*.db
__pycache__/
venv/
```

---

## Step 2: Push to GitHub

### 2.1 Initialize Git Repository (if not already done)
```bash
cd FlaskAuthApp
git init
```

### 2.2 Add All Files
```bash
git add .
git commit -m "Initial commit: Flask Auth App with backend validation"
```

### 2.3 Create Repository on GitHub
1. Go to [github.com](https://github.com)
2. Click "New" repository
3. Name it `FlaskAuthApp`
4. Click "Create repository"

### 2.4 Push to GitHub
```bash
git remote add origin https://github.com/YOUR_USERNAME/FlaskAuthApp.git
git branch -M main
git push -u origin main
```

---

## Step 3: Deploy on Render

### 3.1 Sign Up / Log In to Render
1. Go to [render.com](https://render.com)
2. Sign up with GitHub (recommended)
3. Authorize Render

### 3.2 Create New Web Service
1. Click **"New +"** button (top right)
2. Select **"Web Service"**
3. Click **"Connect account"** to link GitHub
4. Find and select **"FlaskAuthApp"** repository
5. Click **"Connect"**

### 3.3 Configure Service
Fill in the following settings:

| Setting | Value |
|---------|-------|
| **Name** | `flaskapp` (or your preferred name) |
| **Environment** | `Python 3` |
| **Build Command** | `pip install -r requirements.txt && python -c "from app import app, db; app.app_context().push(); db.create_all()"` |
| **Start Command** | `gunicorn app:app` |
| **Instance Type** | Free (Starter) |

### 3.4 Set Environment Variables
Click on **"Environment"** tab:

Add these variables:
```
FLASK_ENV                production
SECRET_KEY               (generate below →)
SESSION_COOKIE_SECURE    True
```

**Generate SECRET_KEY:**
```python
# Run in Python
import secrets
print(secrets.token_hex(32))
```
Copy the output and paste into SECRET_KEY field.

### 3.5 Advanced Settings (Optional)
- **Disk**: Leave default
- **Auto-deploy**: Enabled (redeploys on git push)

### 3.6 Deploy
1. Click **"Create Web Service"**
2. Wait for deployment (2-5 minutes)
3. View logs in real-time
4. Once "Live" appears, your app is deployed!

**Your app URL**: `https://flaskapp.onrender.com` (or custom domain)

---

## Step 4: Configure Database for Production

### Option A: Use Render PostgreSQL (Recommended)

#### 4.1 Create PostgreSQL Database
1. In Render dashboard, click **"New +"** → **"PostgreSQL"**
2. Set **Name**: `flask-db`
3. Set **PostgreSQL Version**: 15
4. Keep other settings default
5. Click **"Create Database"**
6. Wait for creation (1-2 minutes)

#### 4.2 Get Database URL
1. Open your PostgreSQL database from Render dashboard
2. Copy the **External Database URL**
3. Looks like: `postgresql://user:password@host:5432/database`

#### 4.3 Update Web Service
1. Go back to your Web Service
2. Click **"Environment"**
3. Update `DATABASE_URL`:
   ```
   DATABASE_URL    postgresql://user:password@host:5432/database
   ```
4. Click **"Save"**
5. Service will auto-redeploy

### Option B: Use SQLite (Simpler, for Small Projects)
- No additional setup needed
- DATABASE_URL will use SQLite (default in app.py)

---

## Step 5: Verify Deployment

### 5.1 Test Registration
1. Open your app URL: `https://flaskapp.onrender.com`
2. Click **"Register"**
3. Fill in form with test data:
   ```
   Name: John Doe
   Email: john@example.com
   Password: testpass123
   Confirm Password: testpass123
   ```
4. Click **"Create Account"**
5. Should see success message

### 5.2 Test Login
1. Click **"Sign In"**
2. Enter registered credentials
3. Should see **"Dashboard"** with user info

### 5.3 Check Logs
1. Go to Render dashboard
2. Select your service
3. Click **"Logs"** tab
4. Verify no errors

---

## Step 6: Custom Domain (Optional)

### 6.1 Add Custom Domain
1. In your service, click **"Settings"**
2. Scroll to **"Custom Domains"**
3. Click **"Add Custom Domain"**
4. Enter your domain (e.g., `flaskauth.com`)
5. Follow DNS instructions

### 6.2 Update DNS Records
1. Go to your domain registrar
2. Add CNAME record pointing to Render

---

## Step 7: Troubleshooting

### App Keeps Crashing
**Issue**: "Service crashed"

**Solutions**:
1. Check **Logs** in Render dashboard
2. Look for error messages
3. Common cause: Invalid environment variables
4. Verify `FLASK_ENV=production` is set
5. Verify `DATABASE_URL` is correct

### Database Connection Error
**Issue**: "no such relation" or "relation 'users' does not exist"

**Solutions**:
```bash
# Local testing:
python -c "from app import app, db; app.app_context().push(); db.create_all()"

# Or in Render build command, include database init:
python -c "from app import app, db; app.app_context().push(); db.create_all()"
```

### Registration Not Working
**Issue**: Form submits but doesn't create user

**Solutions**:
1. Check database is initialized
2. Verify DATABASE_URL is set
3. Check Render logs for error messages
4. Verify all validation passes

### Static Files Not Loading
**Issue**: CSS/images missing

**Solutions** (if using static files):
```bash
# Add to build command:
python -c "from app import app; app.jinja_env.cache = None"
```

---

## Step 8: Updates & Maintenance

### Deploy Updates
1. Make changes locally
2. Test thoroughly
3. Commit and push:
   ```bash
   git add .
   git commit -m "Describe your changes"
   git push origin main
   ```
4. Render auto-deploys within 30 seconds

### Database Maintenance
```bash
# Local backup SQLite:
cp flaskapp.db flaskapp.db.backup

# PostgreSQL backup (in Render):
# - Automatic backups every day
# - Download from Render dashboard
```

### Monitor Performance
1. Render dashboard → **Metrics**
2. Track CPU, Memory, Network
3. Upgrade instance if needed

---

## Gunicorn Command Explanation

```bash
gunicorn app:app
```

- **`gunicorn`**: Production WSGI server
- **`app`**: Python module name
- **`:app`**: Flask application variable

**For production**, use:
```bash
gunicorn --workers 4 --bind 0.0.0.0:5000 app:app
```

But Render handles this automatically.

---

## Environment Variables for Production

```env
# Essential
FLASK_ENV=production
SECRET_KEY=<64-character-random-hex>
DATABASE_URL=postgresql://... (if using Render PostgreSQL)

# Security
SESSION_COOKIE_SECURE=True
SESSION_COOKIE_HTTPONLY=True
SESSION_COOKIE_SAMESITE=Lax

# Optional
PORT=5000 (Render sets automatically)
DEBUG=False (production default)
```

---

## Production Checklist

Before going live:

- [ ] All code committed and pushed
- [ ] `requirements.txt` complete
- [ ] `Procfile` created
- [ ] `runtime.txt` created
- [ ] `SECRET_KEY` is strong (32+ characters)
- [ ] `FLASK_ENV=production`
- [ ] Database initialized
- [ ] Registration tested
- [ ] Login tested
- [ ] Error handling tested
- [ ] Custom domain configured (if applicable)
- [ ] Monitored first 24 hours for errors
- [ ] Reviewed logs for warnings

---

## Need Help?

- **Render Docs**: [render.com/docs](https://render.com/docs)
- **Flask Docs**: [flask.palletsprojects.com](https://flask.palletsprojects.com)
- **GitHub Issues**: Check your repo issues
- **Error Logs**: Always check Render logs first

---

**Deployment is complete! Your Flask app is now live on the internet. 🚀**
