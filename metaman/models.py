from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)
    quizzes = db.relationship('QuizSession', backref='user', lazy=True)

class QuizSession(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    subject = db.Column(db.String(50), nullable=False)
    difficulty = db.Column(db.String(10), nullable=False)
    score = db.Column(db.Integer)
    total_questions = db.Column(db.Integer)
    timestamp = db.Column(db.DateTime)

class Question(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    subject = db.Column(db.String(50), nullable=False)
    difficulty = db.Column(db.String(10), nullable=False)
    text = db.Column(db.String(255), nullable=False)
    answer = db.Column(db.String(255), nullable=False)
    hint = db.Column(db.String(255), nullable=True)
    explanation = db.Column(db.String(500), nullable=True)
