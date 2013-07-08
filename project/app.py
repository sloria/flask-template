__all__ = ['app', 'db']
from flask import Flask

# flask-peewee bindings
from flask_peewee.db import Database

app = Flask(__name__)
app.config.from_pyfile('settings.py')

db = Database(app)

# Set up cache, task queue, etc.
