#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
import hashlib
import mongoengine
from datetime import datetime

def generate_salt():
    return os.urandom(16).encode('base_64')

def hash_password(password, salt):
    return hashlib.sha512(salt + password).hexdigest()

class User(mongoengine.Document):
    email = mongoengine.StringField(unique=True)

    secret_hash = mongoengine.StringField(required=True)
    salt = mongoengine.StringField(required=True)

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
