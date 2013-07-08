"""
views imports app, auth, and models, but none of these import views
"""
from flask import render_template  # ...etc , redirect, request, url_for
from flask.ext.classy import FlaskView

from app import app
from auth import auth
from models import User


class BaseView(FlaskView):
    '''Basic views, such as the home and about page.'''
    route_base = '/'

    def index(self):
        return render_template('home.html')

    @app.route('/about')
    def about(self):
        return render_template('about.html')


BaseView.register(app)
