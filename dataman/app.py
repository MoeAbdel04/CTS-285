from flask import Flask, render_template, request, redirect, url_for, session
from math_practice import MathPractice, Parent

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Needed for session management

# Global variables to hold the current state
math_practice = MathPractice()
parent = Parent("Bob")

@app.route('/')
def index():
    # Reset session for new practice session
    session.clear()
    return render_template('index.html')

@app.route('/set_difficulty', methods=['POST'])
def set_difficulty():
    global math_practice, parent
    difficulty = request.form['difficulty']
    parent.set_difficulty(math_practice, difficulty)
    session['questions'] = []  # Start tracking questions and answers
    session['score'] = 0  # Start tracking score
    session['total_questions'] = 0  # Total number of questions
    return redirect(url_for('generate_problem'))

@app.route('/generate_problem')
def generate_problem():
    problem, correct_answer = math_practice.generate_problem()
    session['current_problem'] = problem
    session['correct_answer'] = correct_answer
    return render_template('result.html', problem=problem)

@app.route('/check_answer', methods=['POST'])
def check_answer():
    student_answer = request.form['answer']
    feedback = ''
    
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
    # If user chooses to go to the next question, generate a new problem
    if 'next' in request.form:
        return redirect(url_for('generate_problem'))
    
    # If user chooses to quit, display history and grade
    elif 'quit' in request.form:
        return redirect(url_for('show_history'))

@app.route('/show_history')
def show_history():
    total_questions = session.get('total_questions', 0)
    score = session.get('score', 0)
    questions = session.get('questions', [])
    
    # Calculate grade as a percentage
    if total_questions > 0:
        grade = (score / total_questions) * 100
    else:
        grade = 0

    return render_template('history.html', questions=questions, score=score, total_questions=total_questions, grade=grade)

if __name__ == '__main__':
    app.run(debug=True)
