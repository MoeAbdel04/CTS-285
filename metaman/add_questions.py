from app import app, db
from models import Question

# Extended list of questions for better quiz content coverage
questions = [
    # Math - Easy
    {'subject': 'math', 'difficulty': 'easy', 'text': 'What is 5 + 7?', 'answer': '12', 'hint': 'Add the numbers', 'explanation': '5 plus 7 equals 12.'},
    {'subject': 'math', 'difficulty': 'easy', 'text': 'What is 8 - 3?', 'answer': '5', 'hint': 'Subtract the numbers', 'explanation': '8 minus 3 equals 5.'},
    {'subject': 'math', 'difficulty': 'easy', 'text': 'What is 3 * 3?', 'answer': '9', 'hint': 'Multiply the numbers', 'explanation': '3 times 3 equals 9.'},
    {'subject': 'math', 'difficulty': 'easy', 'text': 'What is 15 / 3?', 'answer': '5', 'hint': 'Divide 15 by 3', 'explanation': '15 divided by 3 equals 5.'},
    {'subject': 'math', 'difficulty': 'easy', 'text': 'What is 10 - 6?', 'answer': '4', 'hint': 'Subtract the numbers', 'explanation': '10 minus 6 equals 4.'},

    # Math - Medium
    {'subject': 'math', 'difficulty': 'medium', 'text': 'What is the square root of 49?', 'answer': '7', 'hint': 'Think of a number that when multiplied by itself gives 49', 'explanation': 'The square root of 49 is 7.'},
    {'subject': 'math', 'difficulty': 'medium', 'text': 'What is 9 * 8?', 'answer': '72', 'hint': 'Multiply the numbers', 'explanation': '9 times 8 equals 72.'},
    {'subject': 'math', 'difficulty': 'medium', 'text': 'What is 81 divided by 9?', 'answer': '9', 'hint': 'Think of a number that when multiplied by 9 gives 81', 'explanation': '81 divided by 9 equals 9.'},
    {'subject': 'math', 'difficulty': 'medium', 'text': 'What is 5 squared?', 'answer': '25', 'hint': '5 multiplied by itself', 'explanation': '5 squared equals 25.'},
    {'subject': 'math', 'difficulty': 'medium', 'text': 'What is 12 * 12?', 'answer': '144', 'hint': 'Multiply 12 by itself', 'explanation': '12 times 12 equals 144.'},

    # Math - Hard
    {'subject': 'math', 'difficulty': 'hard', 'text': 'What is the derivative of x^3?', 'answer': '3x^2', 'hint': 'Use the power rule for derivatives', 'explanation': 'The power rule says the derivative of x^n is nx^(n-1).'},
    {'subject': 'math', 'difficulty': 'hard', 'text': 'What is the integral of 2x dx?', 'answer': 'x^2 + C', 'hint': 'Reverse the power rule', 'explanation': 'The integral of 2x is x^2 + C.'},
    {'subject': 'math', 'difficulty': 'hard', 'text': 'What is the value of sin(90 degrees)?', 'answer': '1', 'hint': 'Think of the unit circle', 'explanation': 'sin(90 degrees) is equal to 1.'},
    {'subject': 'math', 'difficulty': 'hard', 'text': 'Solve for x: 2x + 5 = 15', 'answer': '5', 'hint': 'Subtract 5 from both sides, then divide by 2', 'explanation': '2x + 5 = 15 -> 2x = 10 -> x = 5.'},
    {'subject': 'math', 'difficulty': 'hard', 'text': 'What is log base 2 of 8?', 'answer': '3', 'hint': '2 raised to what power gives 8?', 'explanation': 'log base 2 of 8 is 3 because 2^3 = 8.'},

    # Science - Easy
    {'subject': 'science', 'difficulty': 'easy', 'text': 'What planet is known as the Red Planet?', 'answer': 'Mars', 'hint': 'It is named after the Roman god of war', 'explanation': 'Mars is often called the Red Planet because of its reddish appearance.'},
    {'subject': 'science', 'difficulty': 'easy', 'text': 'What gas do plants breathe in?', 'answer': 'Carbon Dioxide', 'hint': 'It’s the opposite of what humans breathe out', 'explanation': 'Plants take in carbon dioxide for photosynthesis.'},
    {'subject': 'science', 'difficulty': 'easy', 'text': 'What is H2O commonly known as?', 'answer': 'Water', 'hint': 'You drink it every day', 'explanation': 'H2O is the chemical formula for water.'},
    {'subject': 'science', 'difficulty': 'easy', 'text': 'How many planets are in the Solar System?', 'answer': '8', 'hint': 'It used to be 9 before Pluto was reclassified', 'explanation': 'There are 8 planets in the Solar System.'},
    {'subject': 'science', 'difficulty': 'easy', 'text': 'What is the largest organ in the human body?', 'answer': 'Skin', 'hint': 'It’s on the outside', 'explanation': 'Skin is the largest organ in the human body.'},

    # Science - Medium
    {'subject': 'science', 'difficulty': 'medium', 'text': 'What is the powerhouse of the cell?', 'answer': 'Mitochondria', 'hint': 'It generates energy for the cell', 'explanation': 'Mitochondria are known as the powerhouse of the cell because they produce energy.'},
    {'subject': 'science', 'difficulty': 'medium', 'text': 'What element does "O" represent on the periodic table?', 'answer': 'Oxygen', 'hint': 'It’s essential for breathing', 'explanation': 'Oxygen is represented by the symbol "O" on the periodic table.'},
    {'subject': 'science', 'difficulty': 'medium', 'text': 'What is the boiling point of water in degrees Celsius?', 'answer': '100', 'hint': 'It’s a round number', 'explanation': 'Water boils at 100 degrees Celsius.'},
    {'subject': 'science', 'difficulty': 'medium', 'text': 'What force keeps us on the ground?', 'answer': 'Gravity', 'hint': 'It starts with a "G"', 'explanation': 'Gravity is the force that pulls objects towards the Earth.'},
    {'subject': 'science', 'difficulty': 'medium', 'text': 'What is the chemical symbol for gold?', 'answer': 'Au', 'hint': 'It’s not obvious', 'explanation': 'The chemical symbol for gold is "Au".'},

    # History - Easy
    {'subject': 'history', 'difficulty': 'easy', 'text': 'Who was the first president of the United States?', 'answer': 'George Washington', 'hint': 'He’s on the one-dollar bill', 'explanation': 'George Washington was the first president of the United States.'},
    {'subject': 'history', 'difficulty': 'easy', 'text': 'In which year did World War II end?', 'answer': '1945', 'hint': 'It’s in the mid-1940s', 'explanation': 'World War II ended in 1945.'},
    {'subject': 'history', 'difficulty': 'easy', 'text': 'Who was known as the "Maid of Orléans"?', 'answer': 'Joan of Arc', 'hint': 'She was a French heroine', 'explanation': 'Joan of Arc was known as the Maid of Orléans.'},
    {'subject': 'history', 'difficulty': 'easy', 'text': 'Which civilization built the pyramids?', 'answer': 'Egyptians', 'hint': 'Think of Africa', 'explanation': 'The Egyptians built the pyramids.'},
    {'subject': 'history', 'difficulty': 'easy', 'text': 'What year did the Titanic sink?', 'answer': '1912', 'hint': 'It’s before World War I', 'explanation': 'The Titanic sank in 1912.'},
]

def add_questions():
    for q in questions:
        question = Question(
            subject=q['subject'],
            difficulty=q['difficulty'],
            text=q['text'],
            answer=q['answer'],
            hint=q['hint'],
            explanation=q['explanation']
        )
        db.session.add(question)
    db.session.commit()
    print("Questions added successfully.")

if __name__ == '__main__':
    with app.app_context():
        add_questions()
