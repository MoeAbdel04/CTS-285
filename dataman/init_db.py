import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)) + '/..')

from dataman.app import db
db.create_all()
print("Database tables created successfully.")