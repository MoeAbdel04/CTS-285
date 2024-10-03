from flask import Flask, render_template, request, redirect, url_for, session, flash
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import timedelta

app = Flask(__name__)
app.secret_key = 'your_secret_key'
app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(minutes=30)  # Keep session alive for 30 minutes

# Database setup (SQLite)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'
login_manager.login_message_category = 'info'

# User model
class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), unique=True, nullable=False)
    password = db.Column(db.String(150), nullable=False)

# User loader for Flask-Login
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# Create the database
with app.app_context():
    db.create_all()

# Home route for the Answer Checker (after login)
@app.route('/')
@login_required
def index():
    print(f'User is authenticated: {current_user.is_authenticated}')  # Debugging
    session.clear()  # Reset session for new practice session
    return redirect(url_for('set_difficulty'))  # Redirecting to the answer checker homepage

# Set difficulty page for the Answer Checker
@app.route('/set_difficulty', methods=['GET', 'POST'])
@login_required
def set_difficulty():
    if request.method == 'POST':
        difficulty = request.form['difficulty']
        session['difficulty'] = difficulty
        return redirect(url_for('generate_problem'))
    return render_template('set_difficulty.html')

# Generate problem route (Answer Checker)
@app.route('/generate_problem')
@login_required
def generate_problem():
    problem = "2 + 2"
    correct_answer = 4
    session['current_problem'] = problem
    session['correct_answer'] = correct_answer
    return render_template('result.html', problem=problem)

# User registration route
@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        # Check if the username already exists
        existing_user = User.query.filter_by(username=username).first()
        if existing_user:
            flash('Username already exists. Please choose a different one.', 'danger')
            return redirect(url_for('signup'))
        
        # If username doesn't exist, create a new user
        hashed_password = generate_password_hash(password, method='pbkdf2:sha256')
        new_user = User(username=username, password=hashed_password)
        db.session.add(new_user)
        db.session.commit()
        
        flash('Account created successfully! Please log in.', 'success')
        return redirect(url_for('login'))
    
    return render_template('signup.html')

# User login route
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User.query.filter_by(username=username).first()

        if user and check_password_hash(user.password, password):
            login_user(user, remember=True)  # Keep the user logged in across browser sessions
            session.permanent = True  # Set session to be permanent
            flash('Login successful! Redirecting...', 'success')
            return redirect(url_for('index'))  # Redirect to the Answer Checker homepage after login
        else:
            flash('Login failed. Please check your username and password.', 'danger')
    
    return render_template('login.html')

# User logout route
@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have been logged out.', 'info')
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(debug=True)
