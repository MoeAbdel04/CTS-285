import os
from flask import Flask, render_template, request, redirect, url_for, session, flash
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, current_user, logout_user, login_required
from werkzeug.security import generate_password_hash, check_password_hash
from math_practice import MathPractice, Parent

app = Flask(__name__)
app.secret_key = os.getenv('SECRET_KEY', 'your_default_secret_key')
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
db = SQLAlchemy(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'
login_manager.login_message_category = 'info'

# User model
class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(60), nullable=False)

    def __repr__(self):
        return f"User('{self.username}', '{self.email}')"

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# Global variables to hold the current state
math_practice = MathPractice()
parent = Parent("Bob")

@app.route('/')
def index():
    session.pop('questions', None)
    session.pop('score', None)
    session.pop('total_questions', None)
    return render_template('index.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    if request.method == 'POST':
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')
        hashed_password = generate_password_hash(password, method='sha256')
        user = User(username=username, email=email, password=hashed_password)
        db.session.add(user)
        db.session.commit()
        flash('Your account has been created!', 'success')
        return redirect(url_for('login'))
    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        user = User.query.filter_by(email=email).first()
        if user and check_password_hash(user.password, password):
            login_user(user)
            return redirect(url_for('index'))
        else:
            flash('Login unsuccessful. Please check email and password', 'danger')
    return render_template('login.html')

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))

@app.route('/set_difficulty', methods=['POST'])
@login_required
def set_difficulty():
    global math_practice, parent
    difficulty = request.form.get('difficulty')
    if difficulty is None:
        return "Difficulty not specified", 400
    parent.set_difficulty(math_practice, difficulty)
    session['questions'] = []
    session['score'] = 0
    session['total_questions'] = 0
    return redirect(url_for('generate_problem'))

@app.route('/generate_problem')
@login_required
def generate_problem():
    problem, correct_answer = math_practice.generate_problem()
    session['current_problem'] = problem
    session['correct_answer'] = correct_answer
    return render_template('result.html', problem=problem)

@app.route('/check_answer', methods=['POST'])
@login_required
def check_answer():
    student_answer = request.form.get('answer')
    feedback = ''
    
    if student_answer is None:
        return "Answer not provided", 400

    try:
        student_answer = float(student_answer)
        correct_answer = session.get('correct_answer')

        session['total_questions'] += 1
        if student_answer == correct_answer:
            feedback = "Correct! Well done!"
            session['score'] += 1
            result = 'Correct'
        else:
            feedback = f"Incorrect. The correct answer was {correct_answer}."
            result = 'Incorrect'
    except ValueError:
        feedback = "Please enter a valid number."
        result = 'Invalid'

    session['questions'].append({
        'problem': session.get('current_problem'),
        'answer': student_answer,
        'result': result
    })

    return render_template('result.html', problem=session['current_problem'], feedback=feedback)

@app.route('/next_question', methods=['POST'])
@login_required
def next_question():
    if 'next' in request.form:
        return redirect(url_for('generate_problem'))
    elif 'quit' in request.form:
        return redirect(url_for('show_history'))

@app.route('/show_history')
@login_required
def show_history():
    total_questions = session.get('total_questions', 0)
    score = session.get('score', 0)
    questions = session.get('questions', [])
    
    if total_questions > 0:
        grade = round((score / total_questions) * 100, 2)
    else:
        grade = 0

    return render_template('history.html', questions=questions, score=score, total_questions=total_questions, grade=grade)

if __name__ == '__main__':
    app.run(debug=True)