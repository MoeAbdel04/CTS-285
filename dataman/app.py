from flask import Flask, render_template, redirect, url_for, flash, request, session, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Length, EqualTo, ValidationError
from werkzeug.security import generate_password_hash, check_password_hash

# Initialize Flask app
app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_secret_key'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize extensions
db = SQLAlchemy(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'

# User model for storing registered users
class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    password = db.Column(db.String(60), nullable=False)
    score = db.Column(db.Integer, default=0)
    total_questions = db.Column(db.Integer, default=0)
    history = db.Column(db.Text)  # Store JSON data (list of questions and answers)

# Form for signup
class SignupForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=3, max=20)])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=6)])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Sign Up')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError('Username is already taken. Please choose a different one.')

# Form for login
class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Login')

# Load user for Flask-Login
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# Home route (index)
@app.route('/')
def home():
    return render_template('base.html')

# Sign up route
@app.route('/signup', methods=['GET', 'POST'])
def signup():
    form = SignupForm()
    if form.validate_on_submit():
        hashed_password = generate_password_hash(form.password.data, method='sha256')
        new_user = User(username=form.username.data, password=hashed_password)
        db.session.add(new_user)
        db.session.commit()
        flash('Account created successfully! Please log in.', 'success')
        return redirect(url_for('login'))
    return render_template('signup.html', form=form)

# Login route
@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user and check_password_hash(user.password, form.password.data):
            login_user(user)
            return redirect(url_for('dashboard'))
        else:
            flash('Login failed. Check username and password.', 'danger')
    return render_template('login.html', form=form)

# Dashboard route (answer checker and history)
@app.route('/dashboard')
@login_required
def dashboard():
    return render_template('dashboard.html', score=current_user.score, total_questions=current_user.total_questions, history=current_user.history)

# Generate problem route
@app.route('/generate_problem')
@login_required
def generate_problem():
    problem, correct_answer = generate_math_problem()
    session['current_problem'] = problem
    session['correct_answer'] = correct_answer
    return jsonify({"problem": problem})

# Check answer route
@app.route('/check_answer', methods=['POST'])
@login_required
def check_answer():
    data = request.get_json()
    student_answer = float(data['answer'])
    correct_answer = session.get('correct_answer')
    
    result = "Incorrect"
    if student_answer == correct_answer:
        current_user.score += 1
        result = "Correct"
    
    current_user.total_questions += 1
    
    # Save question to user history
    new_history_entry = {
        'problem': session.get('current_problem'),
        'answer': student_answer,
        'result': result
    }
    current_user.history = (current_user.history or "") + str(new_history_entry) + "\n"
    
    db.session.commit()

    return jsonify({"feedback": result, "correct_answer": correct_answer})

# Logout route
@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have been logged out.', 'info')
    return redirect(url_for('home'))

# Initialize the database
with app.app_context():
    db.create_all()

if __name__ == '__main__':
    app.run(debug=True)
