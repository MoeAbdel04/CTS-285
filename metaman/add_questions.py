from app import db
from models import Question

questions = [
    {'subject': 'math', 'difficulty': 'easy', 'text': 'What is 5 + 7?', 'answer': '12', 'hint': 'Add the numbers', 'explanation': '5 plus 7 equals 12.'},
    {'subject': 'math', 'difficulty': 'medium', 'text': 'What is the square root of 16?', 'answer': '4', 'hint': '4 multiplied by itself gives 16', 'explanation': 'The square root of 16 is 4.'},
    {'subject': 'science', 'difficulty': 'easy', 'text': 'What is the chemical symbol for water?', 'answer': 'H2O', 'hint': 'Two hydrogen atoms', 'explanation': 'Water is H2O.'}
]

def add_questions():
    for q in questions:
        question = Question(subject=q['subject'], difficulty=q['difficulty'], text=q['text'], answer=q['answer'], hint=q['hint'], explanation=q['explanation'])
        db.session.add(question)
    db.session.commit()
    print("Questions added successfully.")

if __name__ == '__main__':
    with app.app_context():
        add_questions()
