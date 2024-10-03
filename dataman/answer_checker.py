


from math_practice import MathPractice, Parent

# Student class for inputting answers
class Student:
    def __init__(self, name):
        self.name = name

    def input_answer(self, problem, answer):
        print(f"Student {self.name} answered: {answer} for problem: {problem}")
        return answer

# Teacher class for feedback, hints, and explanations
class Teacher:
    def __init__(self, name):
        self.name = name

    def give_feedback(self, student, problem, student_answer, correct_answer):
        if student_answer == correct_answer:
            print(f"Teacher {self.name}: Student {student.name} got the correct answer for problem: {problem}.")
        else:
            print(f"Teacher {self.name}: Student {student.name} needs more practice on problem: {problem}.")

    def provide_hint(self, problem):
        hints = {
            "2+2": "Remember, addition is the process of combining two numbers together.",
            "5*3": "Multiplication is repeated addition. Try adding 5 three times.",
            # Add more hints here
        }
        print(f"Hint for problem {problem}: {hints.get(problem, 'No hint available.')}")
    
    def provide_explanation(self, problem, correct_answer):
        explanations = {
            "2+2": "2+2 equals 4 because when you combine two and two, you get four.",
            "5*3": "5 times 3 equals 15 because multiplication is repeated addition (5+5+5).",
            # Add more explanations here
        }
        print(f"Explanation for problem {problem}: {explanations.get(problem, 'No explanation available.')}")

# Example usage:
if __name__ == "__main__":
    # Create math practice session and set difficulty level
    math_practice = MathPractice()
    parent = Parent("Bob")
    
    # Set difficulty through parent
    difficulty = input("Please select a difficulty level (easy, medium, hard): ").lower()
    parent.set_difficulty(math_practice, difficulty)

    # Generate a math problem
    problem, correct_answer = math_practice.generate_problem()
    print(f"Solve the problem: {problem}")

    # Create student and teacher objects
    student = Student("Alice")
    teacher = Teacher("Mrs. Smith")

    # Student inputs an answer
    try:
        student_answer = float(input("Your answer: "))
        student.input_answer(problem, student_answer)

        # Parent checks the result (view results)
        if student_answer == correct_answer:
            print("Correct! Well done!")
        else:
            print(f"Incorrect. The correct answer was {correct_answer}.")

        # Teacher gives feedback and explanations
        teacher.give_feedback(student, problem, student_answer, correct_answer)

        if student_answer != correct_answer:
            teacher.provide_hint(problem)
        teacher.provide_explanation(problem, correct_answer)
        
    except ValueError:
        print("Please enter a valid number.")
