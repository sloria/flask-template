# -*- coding: utf-8 -*-

from flask_peewee.rest import (RestAPI, RestResource, UserAuthentication,
    AdminAuthentication)

from app import app
from auth import auth
from models import User

user_auth = UserAuthentication(auth)
admin_auth = AdminAuthentication(auth)

# use same credentials as the auth system
# could also use key-based auth
api = RestAPI(app, default_auth=user_auth)

class UserResource(RestResource):
    exclude = ('password', 'email')

# register our models so they are exposed via /api/<model>/
api.register(User, UserResource, auth=admin_auth)
