from flask import Flask, render_template, request, redirect, url_for, session, flash
from werkzeug.security import generate_password_hash, check_password_hash
from models import db, User, QuizSession, Question
from datetime import datetime, timedelta
import random

app = Flask(__name__)
app.config.from_object('config')
app.permanent_session_lifetime = timedelta(minutes=30)
db.init_app(app)

# User Registration
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        hashed_password = generate_password_hash(password, method='pbkdf2:sha256')
        user = User(username=username, password=hashed_password)
        db.session.add(user)
        db.session.commit()
        flash('Registration successful! Please log in.')
        return redirect(url_for('login'))
    return render_template('register.html')

# Login
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User.query.filter_by(username=username).first()
        if user and check_password_hash(user.password, password):
            session['user_id'] = user.id
            session.permanent = True  # Keep the session alive for the set duration
            return redirect(url_for('index'))
        else:
            flash('Invalid credentials. Please try again.')
    return render_template('login.html')

# Index - Select Subject and Difficulty
@app.route('/')
def index():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    subjects = Question.query.with_entities(Question.subject).distinct().all()
    print("Subjects:", subjects)  # Debug print statement
    return render_template('index.html', subjects=[s.subject for s in subjects])

# Quiz Route
@app.route('/quiz/<subject>/<difficulty>')
def quiz(subject, difficulty):
    if 'user_id' not in session:
        return redirect(url_for('login'))
    questions = Question.query.filter_by(subject=subject, difficulty=difficulty).all()

    # Debugging statements
    print(f"Subject: {subject}, Difficulty: {difficulty}")
    print(f"Questions found: {questions}")

    if questions:
        random.shuffle(questions)
        session['quiz_questions'] = [q.id for q in questions]
        session['subject'] = subject
        session['difficulty'] = difficulty
        session['score'] = 0
        session['question_index'] = 0

        # Debug session data
        print("Session after setting up quiz:", session)

        return redirect(url_for('question'))
    else:
        flash('No questions available for this selection.')
        return redirect(url_for('index'))

# Question Route
@app.route('/question', methods=['GET', 'POST'])
def question():
    if 'quiz_questions' not in session:
        flash("No quiz in progress.")
        return redirect(url_for('index'))

    print("Session data at /question:", session)

    if request.method == 'POST':
        user_answer = request.form['answer']
        question_id = session['quiz_questions'][session['question_index']]
        question = Question.query.get(question_id)

        print(f"User Answer: {user_answer}, Correct Answer: {question.answer}")

        if user_answer.lower() == question.answer.lower():
            session['score'] += 1
        session['question_index'] += 1

    if session['question_index'] < len(session['quiz_questions']):
        question = Question.query.get(session['quiz_questions'][session['question_index']])
        return render_template('question.html', question=question)
    else:
        new_session = QuizSession(user_id=session['user_id'], subject=session['subject'],
                                  difficulty=session['difficulty'], score=session['score'],
                                  total_questions=len(session['quiz_questions']), timestamp=datetime.now())
        db.session.add(new_session)
        db.session.commit()
        return redirect(url_for('results'))

# Results Route
@app.route('/results')
def results():
    if 'score' not in session or 'quiz_questions' not in session:
        flash("No quiz results to display.")
        return redirect(url_for('index'))

    score = session.get('score')
    total = len(session['quiz_questions'])
    return render_template('results.html', score=score, total=total)

# Leaderboard
@app.route('/leaderboard')
def leaderboard():
    leaderboard_data = QuizSession.query.order_by(QuizSession.score.desc()).limit(10).all()
    return render_template('leaderboard.html', leaderboard=leaderboard_data)

@app.route('/reset_session')
def reset_session():
    session.clear()
    flash("Session has been reset.")
    return redirect(url_for('index'))

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
