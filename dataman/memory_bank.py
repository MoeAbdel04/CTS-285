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
            num2 = random.randint(50, 100)
            operation = random.choice(["+", "-", "*", "/"])
        else:
            return "Invalid difficulty level."

        problem = f"{num1} {operation} {num2}"
        return problem

# User Story 2: As a parent, I want to set a specific difficulty level for the math problems, so that my child can practice at their appropriate level.
class Parent:
    def __init__(self, name):
        self.name = name

    def set_difficulty(self, math_practice, difficulty):
        print(f"Parent {self.name} has set the difficulty to: {difficulty}")
        math_practice.difficulty = difficulty


# Example usage:

# Creating a math practice session with default difficulty level
math_practice = MathPractice()

# Parent sets difficulty level
parent = Parent("Bob")
parent.set_difficulty(math_practice, "medium")

# Student gets a randomly generated problem based on the difficulty level
problem = math_practice.generate_problem()
print(f"Generated problem: {problem}")