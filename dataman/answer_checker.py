import random

# User Story 1: As a student, I want to input my answers for math problems, so that I can quickly check if I am correct.
class Student:
    def __init__(self, name):
        self.name = name
    
    def input_answer(self, problem, answer):
        print(f"Student {self.name} answered: {answer} for problem: {problem}")
        return answer

# User Story 2: As a parent, I want to see the results of my child’s answers, so that I can understand their progress in math.
class Parent:
    def __init__(self, name, student):
        self.name = name
        self.student = student

    def view_results(self, problem, correct_answer, student_answer):
        if student_answer == correct_answer:
            print(f"Parent {self.name} sees that {self.student.name}'s answer to {problem} is correct.")
        else:
            print(f"Parent {self.name} sees that {self.student.name}'s answer to {problem} is incorrect.")

# User Story 3: As a teacher, I want to receive feedback on my students' performance, so that I can identify areas where they need more practice.
class Teacher:
    def __init__(self, name):
        self.name = name

    def give_feedback(self, student, problem, student_answer, correct_answer):
        if student_answer == correct_answer:
            print(f"Teacher {self.name}: Student {student.name} got the correct answer for problem: {problem}.")
        else:
            print(f"Teacher {self.name}: Student {student.name} needs more practice on problem: {problem}.")

# User Story 4: As a student, I want to receive hints if I get an answer wrong, so that I can learn the correct method.
    def provide_hint(self, problem):
        hints = {
            "2+2": "Remember, addition is the process of combining two numbers together.",
            "5*3": "Multiplication is repeated addition. Try adding 5 three times.",
            # Add more problems and hints as needed
        }
        print(f"Hint for problem {problem}: {hints.get(problem, 'No hint available.')}")
        
# User Story 5: As a teacher, I want the Answer Checker to provide explanations for correct answers, so that I can help students understand their mistakes.
    def provide_explanation(self, problem, correct_answer):
        explanations = {
            "2+2": "2+2 equals 4 because when you combine two and two, you get four.",
            "5*3": "5 times 3 equals 15 because multiplication is repeated addition (5+5+5).",
            # Add more problems and explanations as needed
        }
        print(f"Explanation for problem {problem}: {explanations.get(problem, 'No explanation available.')}")

# Ensure division problems don't result in fractions
def generate_problem(difficulty="easy"):
    if difficulty == "easy":
        num1 = random.randint(1, 10)
        num2 = random.randint(1, 10)
        operation = random.choice(["+", "-"])
    elif difficulty == "medium":
        num1 = random.randint(10, 50)
        num2 = random.randint(10, 50)
        operation = random.choice(["+", "-", "*"])
    elif difficulty == "hard":
        num1 = random.randint(50, 100)
        num2 = random.randint(1, 50)  # To avoid division by zero
        operation = random.choice(["+", "-", "*", "/"])
        # Ensure division results in an integer by making num1 divisible by num2
        if operation == "/":
            num1 = num2 * random.randint(1, 10)
    else:
        return "Invalid difficulty level."

    problem = f"{num1} {operation} {num2}"
    correct_answer = eval(problem)
    return problem, correct_answer

# Example usage:

# Creating objects
student = Student("Alice")
parent = Parent("Bob", student)
teacher = Teacher("Mrs. Smith")

# Generate a math problem with difficulty level 'medium'
problem, correct_answer = generate_problem(difficulty="medium")

# Student inputs an answer
student_answer = student.input_answer(problem, 80)

# Parent checks the result
parent.view_results(problem, correct_answer, student_answer)

# Teacher gives feedback
teacher.give_feedback(student, problem, student_answer, correct_answer)

# If answer is wrong, teacher provides a hint
if student_answer != correct_answer:
    teacher.provide_hint(problem)

# Teacher provides explanation for the correct answer
teacher.provide_explanation(problem, correct_answer)
