# -*- coding: utf-8 -*-

"""
models imports app, but app does not import models so we haven't created
any loops.
"""
import datetime

from flask_peewee.auth import BaseUser  # provides password helpers..
from peewee import *

from .app import db


class User(db.Model, BaseUser):

    username = CharField()
    password = CharField()
    email = CharField()
    join_date = DateTimeField(default=datetime.datetime.now)
    active = BooleanField(default=True)
    admin = BooleanField(default=False)

    def __unicode__(self):
        return self.username
