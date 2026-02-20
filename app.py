from flask import Flask, render_template, request, redirect, url_for, flash
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
import os
from config import config
from models import db, User

# Initialize Flask app
app = Flask(__name__)

# Load configuration
config_name = os.environ.get('FLASK_ENV', 'development')
app.config.from_object(config.get(config_name, config['development']))

# Initialize extensions
db.init_app(app)
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'
login_manager.login_message = 'Please log in to access this page.'
login_manager.login_message_category = 'info'

# Load user callback
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# Create app context
with app.app_context():
    db.create_all()

# ============================================================================
# VALIDATION HELPER FUNCTIONS
# ============================================================================

def validate_registration_input(name, email, password, password_confirm):
    """
    Validate registration form input.
    Returns: (is_valid, error_message)
    """
    # Strip whitespace from inputs
    name = name.strip() if name else ''
    email = email.strip() if email else ''
    password = password.strip() if password else ''
    password_confirm = password_confirm.strip() if password_confirm else ''
    
    # Validate name
    if not name:
        return False, 'Name is required.'
    
    if len(name) < 2:
        return False, 'Name must be at least 2 characters long.'
    
    if len(name) > 120:
        return False, 'Name must not exceed 120 characters.'
    
    # Validate email
    if not email:
        return False, 'Email is required.'
    
    # Basic email validation
    if '@' not in email or '.' not in email.split('@')[-1]:
        return False, 'Please enter a valid email address.'
    
    if len(email) > 120:
        return False, 'Email must not exceed 120 characters.'
    
    # Check if email already exists
    existing_user = User.query.filter_by(email=email.lower()).first()
    if existing_user:
        return False, 'Email already registered. Please use a different email or log in.'
    
    # Validate password
    if not password:
        return False, 'Password is required.'
    
    if len(password) < 6:
        return False, 'Password must be at least 6 characters long.'
    
    if len(password) > 255:
        return False, 'Password must not exceed 255 characters.'
    
    # Validate password confirmation
    if not password_confirm:
        return False, 'Password confirmation is required.'
    
    if password != password_confirm:
        return False, 'Passwords do not match.'
    
    return True, None

# ============================================================================
# ROUTES
# ============================================================================

@app.route('/')
def index():
    """Home page"""
    if current_user.is_authenticated:
        return redirect(url_for('dashboard'))
    return redirect(url_for('register'))

@app.route('/register', methods=['GET', 'POST'])
def register():
    """Register a new user with backend validation"""
    
    # If user is already authenticated, redirect to dashboard
    if current_user.is_authenticated:
        return redirect(url_for('dashboard'))
    
    if request.method == 'POST':
        # Get form data
        name = request.form.get('name', '')
        email = request.form.get('email', '')
        password = request.form.get('password', '')
        password_confirm = request.form.get('password_confirm', '')
        
        # Validate input
        is_valid, error_message = validate_registration_input(name, email, password, password_confirm)
        
        if not is_valid:
            flash(error_message, 'danger')
            # Return to register page with form data (except password)
            return render_template('register.html', 
                                 name=name, 
                                 email=email), 400
        
        try:
            # Create new user (convert email to lowercase for consistency)
            user = User(
                name=name.strip(),
                email=email.strip().lower()
            )
            user.set_password(password)
            
            # Add to database
            db.session.add(user)
            db.session.commit()
            
            flash('Registration successful! Please log in.', 'success')
            return redirect(url_for('login'))
        
        except Exception as e:
            db.session.rollback()
            flash('An error occurred during registration. Please try again.', 'danger')
            app.logger.error(f'Registration error: {str(e)}')
            return render_template('register.html', 
                                 name=name, 
                                 email=email), 500
    
    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    """User login"""
    
    if current_user.is_authenticated:
        return redirect(url_for('dashboard'))
    
    if request.method == 'POST':
        email = request.form.get('email', '').strip()
        password = request.form.get('password', '').strip()
        remember = request.form.get('remember', False)
        
        if not email or not password:
            flash('Email and password are required.', 'danger')
            return render_template('login.html'), 400
        
        user = User.query.filter_by(email=email.lower()).first()
        
        if user and user.check_password(password):
            login_user(user, remember=remember)
            next_page = request.args.get('next')
            return redirect(next_page or url_for('dashboard'))
        
        flash('Invalid email or password.', 'danger')
        return render_template('login.html', email=email), 401
    
    return render_template('login.html')

@app.route('/dashboard')
@login_required
def dashboard():
    """User dashboard (protected route)"""
    return render_template('dashboard.html', user=current_user)

@app.route('/logout')
@login_required
def logout():
    """Logout user"""
    logout_user()
    flash('You have been logged out.', 'success')
    return redirect(url_for('login'))

# ============================================================================
# ERROR HANDLERS
# ============================================================================

@app.errorhandler(404)
def page_not_found(error):
    """Handle 404 errors"""
    return render_template('error.html', 
                         code=404, 
                         message='Page not found.'), 404

@app.errorhandler(500)
def internal_error(error):
    """Handle 500 errors"""
    db.session.rollback()
    return render_template('error.html', 
                         code=500, 
                         message='Internal server error.'), 500

@app.errorhandler(403)
def forbidden(error):
    """Handle 403 errors"""
    return render_template('error.html', 
                         code=403, 
                         message='Access forbidden.'), 403

# ============================================================================
# CLI COMMANDS
# ============================================================================

@app.cli.command()
def init_db():
    """Initialize the database."""
    db.create_all()
    print('Database initialized.')

@app.cli.command()
def drop_db():
    """Drop all database tables."""
    if input('Are you sure? (y/n): ').lower() == 'y':
        db.drop_all()
        print('Database dropped.')

# ============================================================================
# MAIN
# ============================================================================

if __name__ == '__main__':
    app.run(
        host='0.0.0.0',
        port=int(os.environ.get('PORT', 5000)),
        debug=app.config['DEBUG']
    )
