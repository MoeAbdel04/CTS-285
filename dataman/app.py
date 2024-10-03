
from flask import Flask, render_template, request, redirect, url_for
from math_practice import MathPractice, Parent

app = Flask(__name__)

# Global variables to hold the current state
math_practice = MathPractice()
parent = Parent("Bob")
current_problem = None
correct_answer = None

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/set_difficulty', methods=['POST'])
def set_difficulty():
    global math_practice, parent
    difficulty = request.form['difficulty']
    parent.set_difficulty(math_practice, difficulty)
    return redirect(url_for('generate_problem'))

@app.route('/generate_problem')
def generate_problem():
    global current_problem, correct_answer
    current_problem, correct_answer = math_practice.generate_problem()
    return render_template('result.html', problem=current_problem)

@app.route('/check_answer', methods=['POST'])
def check_answer():
    global correct_answer
    student_answer = request.form['answer']
    
    try:
        student_answer = float(student_answer)
        if student_answer == correct_answer:
            feedback = "Correct! Well done!"
        else:
            feedback = f"Incorrect. The correct answer was {correct_answer}."
    except ValueError:
        feedback = "Please enter a valid number."

    return render_template('result.html', problem=current_problem, feedback=feedback)

if __name__ == '__main__':
    app.run(debug=True)
