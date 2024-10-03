import random

# Memory Bank for storing user stories

# User Story 1: As a student, I want to practice randomly generated math problems, so that I can improve my math skills in a fun way.
class MathPractice:
    def __init__(self, difficulty="easy"):
        self.difficulty = difficulty

    def generate_problem(self):
        if self.difficulty == "easy":
            num1 = random.randint(1, 10)
            num2 = random.randint(1, 10)
            operation = random.choice(["+", "-"])
        elif self.difficulty == "medium":
            num1 = random.randint(10, 50)
            num2 = random.randint(10, 50)
            operation = random.choice(["+", "-", "*"])
        elif self.difficulty == "hard":
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

# User Story 2: As a parent, I want to set a specific difficulty level for the math problems, so that my child can practice at their appropriate level.
class Parent:
    def __init__(self, name):
        self.name = name

    def set_difficulty(self, math_practice, difficulty):
        print(f"Parent {self.name} has set the difficulty to: {difficulty}")
        math_practice.difficulty = difficulty

# Main program loop
def main():
    # Create math practice session
    math_practice = MathPractice()

    # Ask user to input difficulty level
    print("Welcome to the Math Practice Program!")
    difficulty = input("Please select a difficulty level (easy, medium, hard): ").lower()

    # Parent sets the difficulty level
    parent = Parent("Bob")
    parent.set_difficulty(math_practice, difficulty)

    # Generate a random math problem
    problem, correct_answer = math_practice.generate_problem()
    print(f"Solve the problem: {problem}")

    # Get student's answer
    try:
        student_answer = float(input("Your answer: "))
        if student_answer == correct_answer:
            print("Correct! Well done!")
        else:
            print(f"Incorrect. The correct answer was {correct_answer}.")
    except ValueError:
        print("Please enter a valid number.")

if __name__ == "__main__":
    main()
