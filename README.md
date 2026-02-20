# Flask Auth App

A professional, production-ready Flask authentication application with secure user registration and login functionality.

## 🎯 Features

- ✅ **Secure User Registration** with comprehensive backend validation
- ✅ **Password Hashing** using Werkzeug's secure hashing (PBKDF2-SHA256)
- ✅ **SQLAlchemy ORM** for database management
- ✅ **Flask-Login** for session management
- ✅ **Input Validation** - name, email, password with detailed error messages
- ✅ **Email Uniqueness** - prevents duplicate email registrations
- ✅ **Flash Messages** for user feedback
- ✅ **Responsive UI** with Bootstrap 5
- ✅ **Error Handling** with custom error pages (404, 500, 403)
- ✅ **Environment Configuration** for different deployment stages
- ✅ **Security Best Practices** - CSRF protection, secure cookies
- ✅ **Production Ready** - optimized for Render, Heroku, or VPS deployment

## 📋 Validation Requirements Met

### Registration Form Validation

| Requirement | Details | Status |
|------------|---------|--------|
| Name Required | Must not be empty | ✅ |
| Name Length | At least 2 characters | ✅ |
| Email Required | Must not be empty | ✅ |
| Email Format | Valid email format | ✅ |
| Email Unique | No duplicate emails | ✅ |
| Password Required | Must not be empty | ✅ |
| Password Length | Minimum 6 characters | ✅ |
| Password Confirm | Passwords must match | ✅ |
| Secure Hashing | PBKDF2-SHA256 | ✅ |
| Error Messages | Clear, user-friendly | ✅ |
| Stay on Form | Validation failure keeps user on form | ✅ |

## 🚀 Quick Start

### Local Development

1. **Clone the repository**
   ```bash
   git clone https://github.com/yourusername/FlaskAuthApp.git
   cd FlaskAuthApp
   ```

2. **Create and activate virtual environment**
   ```bash
   # Windows
   python -m venv venv
   venv\Scripts\activate
   
   # macOS/Linux
   python3 -m venv venv
   source venv/bin/activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Create `.env` file** (copy from `.env.example`)
   ```bash
   cp .env.example .env
   ```

5. **Initialize the database**
   ```bash
   flask init-db
   ```

6. **Run the application**
   ```bash
   flask run
   ```
   
   The app will be available at `http://localhost:5000`

## 🏗️ Project Structure

```
FlaskAuthApp/
├── app.py                 # Main Flask application with routes
├── models.py             # SQLAlchemy database models
├── config.py             # Configuration for different environments
├── requirements.txt      # Python dependencies
├── Procfile              # Render deployment configuration
├── .env.example          # Example environment variables
├── .gitignore            # Git ignore rules
├── README.md             # This file
├── templates/
│   ├── base.html         # Base template with common styling
│   ├── navbar.html       # Navigation bar (included in base)
│   ├── register.html     # Registration form
│   ├── login.html        # Login form
│   ├── dashboard.html    # User dashboard (protected)
│   └── error.html        # Error page (404, 500, 403)
└── flaskapp.db          # SQLite database (auto-created)
```

## 🔐 Security Features

### Password Security
- **Hashing Algorithm**: PBKDF2-SHA256 (industry standard)
- **Werkzeug Integration**: Uses `werkzeug.security.generate_password_hash()`
- **Password Verification**: Secure comparison with `check_password_hash()`

### Form Security
- **CSRF Protection**: Built-in Flask WTF protection
- **Input Validation**: All inputs validated on backend
- **XSS Prevention**: Template auto-escaping enabled
- **SQL Injection Prevention**: SQLAlchemy parameterized queries

### Session Security
- **Secure Cookies**: HTTPOnly, SameSite, Secure flags
- **Session Timeout**: 7-day default timeout
- **Login Required**: Protected routes with `@login_required`

### Email Security
- **Duplicate Prevention**: Unique constraint on email field
- **Case-Insensitive**: Emails stored/compared in lowercase
- **Format Validation**: Basic email format validation

## 🗂️ Database Schema

### Users Table

```sql
CREATE TABLE users (
    id INTEGER PRIMARY KEY,
    name VARCHAR(120) NOT NULL,
    email VARCHAR(120) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP
);
```

## 🔌 API Endpoints

| Route | Method | Description | Auth Required |
|-------|--------|-------------|----------------|
| `/` | GET | Home (redirects to register or dashboard) | ❌ |
| `/register` | GET, POST | User registration form | ❌ |
| `/login` | GET, POST | User login form | ❌ |
| `/dashboard` | GET | User dashboard | ✅ |
| `/logout` | GET | Logout user | ✅ |

## 🌐 Deployment

### Deploy on Render

1. **Push to GitHub**
   ```bash
   git add .
   git commit -m "Initial commit"
   git push origin main
   ```

2. **Create Render Account**
   - Go to [https://render.com](https://render.com)
   - Sign up or log in

3. **Create New Web Service**
   - Click "New +" → "Web Service"
   - Connect your GitHub repository
   - Select the repository

4. **Configure Service**
   - **Name**: FlaskAuthApp
   - **Environment**: Python 3
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `gunicorn app:app`

5. **Set Environment Variables**
   In Render dashboard, go to "Environment":
   ```
   FLASK_ENV=production
   SECRET_KEY=<generate-a-strong-secret-key>
   DATABASE_URL=<your-postgresql-database-url>
   SESSION_COOKIE_SECURE=True
   ```

6. **Deploy**
   - Click "Deploy"
   - Wait for deployment to complete
   - Your app will be available at `https://your-app-name.onrender.com`

### Deploy on Heroku (Legacy)

```bash
# Install Heroku CLI
# Login to Heroku
heroku login

# Create Heroku app
heroku create your-app-name

# Set environment variables
heroku config:set FLASK_ENV=production
heroku config:set SECRET_KEY=<your-secret-key>
heroku config:set DATABASE_URL=<postgresql-url>

# Deploy
git push heroku main

# View logs
heroku logs --tail
```

### Deploy on VPS (DigitalOcean, Linode, etc.)

**Using Gunicorn + Nginx:**

```bash
# SSH into your server
ssh root@your_server_ip

# Install Python and dependencies
apt-get update
apt-get install python3-pip python3-venv nginx supervisor

# Clone repository
git clone https://github.com/yourusername/FlaskAuthApp.git
cd FlaskAuthApp

# Create virtual environment
python3 -m venv venv
source venv/bin/activate

# Install requirements
pip install -r requirements.txt

# Create .env file with production settings
nano .env

# Initialize database
flask init-db

# Create Supervisor config
sudo nano /etc/supervisor/conf.d/flaskapp.conf
```

**Supervisor Configuration** (`/etc/supervisor/conf.d/flaskapp.conf`):
```ini
[program:flaskapp]
directory=/home/username/FlaskAuthApp
command=/home/username/FlaskAuthApp/venv/bin/gunicorn -w 4 -b 127.0.0.1:8000 app:app
autostart=true
autorestart=true
user=www-data
redirect_stderr=true
stdout_logfile=/var/log/flaskapp.log
```

**Nginx Configuration** (`/etc/nginx/sites-available/flaskapp`):
```nginx
server {
    listen 80;
    server_name your_domain.com;

    location / {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```

## 🔑 Environment Variables

Create a `.env` file in the root directory:

```bash
# Flask Configuration
FLASK_ENV=production              # development, production, testing
SECRET_KEY=your-secret-key-here   # Use strong random key in production
PORT=5000                          # Default port

# Database
DATABASE_URL=sqlite:///flaskapp.db # SQLite for dev, PostgreSQL for prod

# Security
SESSION_COOKIE_SECURE=True         # True for HTTPS only (production)
```

### Generate Secure Secret Key

```python
import secrets
print(secrets.token_hex(32))
```

## 🧪 Testing

### Manual Testing Checklist

- [ ] Register with valid data
- [ ] Attempt register with empty name
- [ ] Attempt register with empty email
- [ ] Attempt register with empty password
- [ ] Attempt register with short password (<6 chars)
- [ ] Attempt register with non-matching passwords
- [ ] Attempt register with duplicate email
- [ ] Login with valid credentials
- [ ] Attempt login with wrong password
- [ ] Verify session persists across pages
- [ ] Test logout functionality
- [ ] Test protected route access

## 📊 Error Handling

The application includes comprehensive error handling:

- **400 Bad Request**: Invalid form submission (validation failure)
- **401 Unauthorized**: Invalid login credentials
- **403 Forbidden**: Access denied (not authenticated)
- **404 Not Found**: Page not found
- **500 Internal Server Error**: Server error with rollback

All errors display user-friendly messages with recovery options.

## 🛠️ Troubleshooting

### Database Issues
```bash
# Reset database (local development only)
flask drop-db

# Reinitialize
flask init-db
```

### Port Already in Use
```bash
# Change port
flask run --port 5001
```

### Import Errors
```bash
# Reinstall dependencies
pip install -r requirements.txt --force-reinstall
```

### Render Deployment Issues

**App crashes immediately:**
1. Check Render logs in the dashboard
2. Verify environment variables are set
3. Ensure Procfile is correct: `web: gunicorn app:app`
4. Check requirements.txt has all dependencies

**Database connection error:**
1. Verify DATABASE_URL format
2. Test connection string locally
3. Ensure database service is running

## 📦 Dependencies

| Package | Version | Purpose |
|---------|---------|---------|
| Flask | 3.0.0 | Web framework |
| Flask-SQLAlchemy | 3.1.1 | ORM |
| Flask-Login | 0.6.3 | Session management |
| Flask-Migrate | 4.0.5 | Database migrations |
| Werkzeug | 3.0.1 | Security utilities |
| SQLAlchemy | 2.0.23 | Database toolkit |
| Gunicorn | 21.2.0 | Production WSGI server |
| python-dotenv | 1.0.0 | Environment variables |

## 🚨 Production Checklist

Before deploying to production:

- [ ] Set `FLASK_ENV=production`
- [ ] Generate strong `SECRET_KEY`
- [ ] Enable `SESSION_COOKIE_SECURE=True`
- [ ] Use PostgreSQL instead of SQLite
- [ ] Set up HTTPS/SSL certificate
- [ ] Configure proper database backups
- [ ] Set up error logging and monitoring
- [ ] Enable rate limiting for login/register
- [ ] Set up CORS if needed
- [ ] Review security headers
- [ ] Test all validation scenarios
- [ ] Verify error messages don't leak sensitive info

## 📝 License

MIT License - Feel free to use this for personal and commercial projects.

## 🤝 Contributing

Contributions are welcome! Please follow these steps:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 💬 Support

For issues and questions:
- Open an issue on GitHub
- Check existing documentation
- Review error logs in production

## 👨‍💼 Author

Created as a professional Flask authentication template.

---

**Built with ❤️ using Flask, SQLAlchemy, and security best practices**
