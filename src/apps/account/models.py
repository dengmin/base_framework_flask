#! /usr/bin/env python
#coding=utf-8

from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
from random import choice
from src.database import db


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100),unique=True,index=True)
    email = db.Column(db.String(200), unique=True, nullable=False, index=True)
    password = db.Column(db.String(100), nullable=False)
    website = db.Column(db.String(400))
    role = db.Column(db.Integer, default=1)
    token = db.Column(db.String(16))
    created = db.Column(db.DateTime, default=datetime.utcnow)
    city = db.Column(db.String(200))
    description = db.Column(db.Text)

    def __init__(self, email, **kwargs):
        self.email = email.lower()
        
        if 'password' in kwargs:
            raw = kwargs.pop('password')
            self.password = self.generate_password_hash(raw)
        for k, v in kwargs.items():
            setattr(self, k, v)

    def check_password(self, raw):
        return check_password_hash(self.password, raw)

    @staticmethod
    def create_token(length=16):
        chars = ('0123456789'
                'abcdefghijklmnopqrstuvwxyz'
                'ABCDEFGHIJKLMNOPQRSTUVWXYZ')
        salt = ''.join([choice(chars) for i in range(length)])
        return salt
