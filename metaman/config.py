import os

SECRET_KEY = os.environ.get('SECRET_KEY') or 'your_secret_key'
SQLALCHEMY_DATABASE_URI = 'sqlite:///answer_checker.db'
SQLALCHEMY_TRACK_MODIFICATIONS = False
