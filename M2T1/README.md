M2T1 - Webapp #1
goals:
to learn basic Flask programming
to be able to repeat a server config
maybe to have fun
lessons learned
bash commands you cannot live without:

- ls <- what's in this directory
- cd <- change directory
source <- run a script (like activate)
instructions
initial tutorial: https://blog.pythonanywhere.com/121/ but we're using codespaces instead of PA

install library:

first set up virtualenvironment

- pip install virtualenv
- cd M2T1

- virtualenv venv
source venv/bin/activate now we have our "venv" environment, so we can install things in it. to turn it off:
deactivate
start installing requirements:

- pip install flask
- pip freeze > requirements.txt
now we can write our minimal Flask app to test it TODO: write a Flask app that does something useful!

to start:

- flask --debug --app hello run

