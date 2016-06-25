#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os, hashlib, mongoengine, config
from datetime import datetime
from pushnotify import pushover

def generate_salt():
    return os.urandom(16).encode('base_64')

def hash_password(password, salt):
    return hashlib.sha512(salt + password).hexdigest()

class User(mongoengine.Document):
    email = mongoengine.StringField(unique=True)

    secret_hash = mongoengine.StringField(required=True)
    salt = mongoengine.StringField(required=True)

    pushover_user = mongoengine.StringField()
    subscribedAd = mongoengine.ListField()

    def notify(self, title, msg):
        if not self.pushover_user:
            return

        c = pushover.Client(config.pushover_app_token)
        c.add_key(self.pushover_user)
        c.notify(msg, title)

    def __hash__(self):
        return hash(self.email)

    @staticmethod
    def new_user(email, password):
        user = User(email=email)

        user.salt = generate_salt()
        user.secret_hash = hash_password(password, user.salt)

        return user

    def clean(self):
        self.email = self.email.lower()

    def valid_password(self, password):
        return hash_password(password, self.salt) == self.secret_hash
