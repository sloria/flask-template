"""
Single entry-point that resolves the
import dependencies. Blueprints could be imported here.

This file is also used to run the app:
    python main.py
"""
import os
from .app import app, db

from .auth import *
from .admin import admin
from .api import api
from .models import *
from .views import *

admin.setup()
api.setup()

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)