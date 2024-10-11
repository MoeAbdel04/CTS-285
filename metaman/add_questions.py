from app import app, db
from models import Question

questions = [
    # Math - Easy
    {'subject': 'math', 'difficulty': 'easy', 'text': 'What is 5 + 7?', 'answer': '12', 'hint': 'Add the numbers', 'explanation': '5 plus 7 equals 12.'},
    {'subject': 'math', 'difficulty': 'easy', 'text': 'What is 9 - 3?', 'answer': '6', 'hint': 'Subtract the numbers', 'explanation': '9 minus 3 equals 6.'},
    # Math - Medium
    {'subject': 'math', 'difficulty': 'medium', 'text': 'What is the square root of 49?', 'answer': '7', 'hint': '7 multiplied by itself gives 49', 'explanation': 'The square root of 49 is 7.'},
    {'subject': 'math', 'difficulty': 'medium', 'text': 'What is 12 * 12?', 'answer': '144', 'hint': 'It is in the 12 multiplication table', 'explanation': '12 multiplied by 12 is 144.'},
    # Math - Hard
    {'subject': 'math', 'difficulty': 'hard', 'text': 'What is 125 divided by 5?', 'answer': '25', 'hint': 'It involves dividing a 3-digit number', 'explanation': '125 divided by 5 is 25.'},
    {'subject': 'math', 'difficulty': 'hard', 'text': 'What is the cube root of 27?', 'answer': '3', 'hint': 'What number multiplied by itself 3 times gives 27?', 'explanation': 'The cube root of 27 is 3.'},
    
    # Science - Easy
    {'subject': 'science', 'difficulty': 'easy', 'text': 'What is the chemical symbol for water?', 'answer': 'H2O', 'hint': 'Two hydrogen atoms and one oxygen atom', 'explanation': 'Water is H2O.'},
    {'subject': 'science', 'difficulty': 'easy', 'text': 'What planet is known as the Red Planet?', 'answer': 'Mars', 'hint': 'It is named after the Roman god of war', 'explanation': 'Mars is known as the Red Planet.'},
    # Science - Medium
    {'subject': 'science', 'difficulty': 'medium', 'text': 'What is the hardest natural substance on Earth?', 'answer': 'Diamond', 'hint': 'It is a form of carbon', 'explanation': 'Diamond is the hardest natural substance.'},
    {'subject': 'science', 'difficulty': 'medium', 'text': 'What gas do plants absorb from the atmosphere?', 'answer': 'Carbon Dioxide', 'hint': 'It is essential for photosynthesis', 'explanation': 'Plants absorb carbon dioxide for photosynthesis.'},
    # Science - Hard
    {'subject': 'science', 'difficulty': 'hard', 'text': 'What is the powerhouse of the cell?', 'answer': 'Mitochondria', 'hint': 'It produces energy for the cell', 'explanation': 'The mitochondria is known as the powerhouse of the cell.'},
    {'subject': 'science', 'difficulty': 'hard', 'text': 'What is the atomic number of oxygen?', 'answer': '8', 'hint': 'It’s a single-digit number', 'explanation': 'The atomic number of oxygen is 8.'}
]

def add_questions():
    # Check if there are existing questions
    if Question.query.first() is None:
        for q in questions:
            question = Question(subject=q['subject'], difficulty=q['difficulty'], text=q['text'], answer=q['answer'], hint=q['hint'], explanation=q['explanation'])
            db.session.add(question)
        db.session.commit()
        print("Questions added successfully.")
    else:
        print("Questions already exist. No need to add again.")

if __name__ == '__main__':
    with app.app_context():
        add_questions()
