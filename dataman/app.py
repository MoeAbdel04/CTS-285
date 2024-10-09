import os
from flask import Flask, render_template, request, redirect, url_for, session, flash
from werkzeug.security import generate_password_hash, check_password_hash
from math_practice import MathPractice, Parent
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.secret_key = os.getenv('SECRET_KEY', 'your_default_secret_key')
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
db = SQLAlchemy(app)

# User model
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(120), nullable=False)

# Create tables
with app.app_context():
    db.create_all()

# Global variables to hold the current state
math_practice = MathPractice()
parent = Parent("Bob")

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User.query.filter_by(username=username).first()
        if user and check_password_hash(user.password, password):
            session['user_id'] = user.id
            flash('Logged in successfully.', 'success')
            return redirect(url_for('index'))
        else:
            flash('Invalid username or password', 'error')
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        if len(password) < 8:
            flash('Password must be at least 8 characters long', 'error')
            return render_template('register.html')
        
        existing_user = User.query.filter_by(username=username).first()
        if existing_user:
            flash('Username already exists', 'error')
        else:
            hashed_password = generate_password_hash(password)
            new_user = User(username=username, password=hashed_password)
            db.session.add(new_user)
            db.session.commit()
            flash('Registered successfully. Please log in.', 'success')
            return redirect(url_for('login'))
    return render_template('register.html')

@app.route('/logout')
def logout():
    session.pop('user_id', None)
    flash('Logged out successfully.', 'success')
    return redirect(url_for('login'))

@app.route('/')
def index():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    # Reset specific session data for new practice session
    session.pop('questions', None)
    session.pop('score', None)
    session.pop('total_questions', None)
    return render_template('index.html')

@app.route('/set_difficulty', methods=['POST'])
def set_difficulty():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    global math_practice, parent
    difficulty = request.form.get('difficulty')
    if difficulty is None:
        return "Difficulty not specified", 400
    parent.set_difficulty(math_practice, difficulty)
    session['questions'] = []  # Start tracking questions and answers
    session['score'] = 0  # Start tracking score
    session['total_questions'] = 0  # Total number of questions
    return redirect(url_for('generate_problem'))

@app.route('/generate_problem')
def generate_problem():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    problem, correct_answer = math_practice.generate_problem()
    session['current_problem'] = problem
    session['correct_answer'] = correct_answer
    return render_template('result.html', problem=problem)

@app.route('/check_answer', methods=['POST'])
def check_answer():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    student_answer = request.form.get('answer')
    feedback = ''
    
    if student_answer is None:
        return "Answer not provided", 400

    try:
        student_answer = float(student_answer)
        correct_answer = session.get('correct_answer')

        # Update session tracking
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

    # Append the result to the session's question history
    session['questions'].append({
        'problem': session.get('current_problem'),
        'answer': student_answer,
        'result': result
    })

    return render_template('result.html', problem=session['current_problem'], feedback=feedback)

@app.route('/next_question', methods=['POST'])
def next_question():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    # If user chooses to go to the next question, generate a new problem
    if 'next' in request.form:
        return redirect(url_for('generate_problem'))
    
    # If user chooses to quit, display history and grade
    elif 'quit' in request.form:
        return redirect(url_for('show_history'))

@app.route('/show_history')
def show_history():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    total_questions = session.get('total_questions', 0)
    score = session.get('score', 0)
    questions = session.get('questions', [])
    
    # Calculate grade as a percentage and round to 2 decimal places
    if total_questions > 0:
        grade = round((score / total_questions) * 100, 2)
    else:
        grade = 0

    return render_template('history.html', questions=questions, score=score, total_questions=total_questions, grade=grade)

if __name__ == '__main__':
    app.run(debug=True)