Metaman --- testing flask integration 


SETTING UP VENV
- Install virtual env with: python -m virtualenv venv

- source venv/bin/activate

- pip install flask



INSTALL REQUIRMENTS TO RUN APP
- pip install -r requirements.txt

- pip freeze > requirements.txt




ADDS QUESTIONS TO DATABASE
- python add_questions.py



RUN APP
- cd (folder name) to run commands in the folder for the program

- set SECRET_KEY=your_secret_key

- flask --debug --app app run

- Control c to quit