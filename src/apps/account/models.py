#! /usr/bin/env python
#coding=utf-8

from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug import cached_property
from flask.ext.sqlalchemy import BaseQuery
from flask_principal import RoleNeed, UserNeed, Permission
from datetime import datetime
from src.database import db
from src.core.permission import adminNeed,vipNeed,loginNeed

class UserQuery(BaseQuery):
    def from_identity(self, identity):
        try:
            user = self.get(int(identity.name))
        except:
            user = None
        if user:
            identity.provides.update(user.provides)
        identity.user = user
        return user
    
    def get_by_username(self,userName):
        user = self.filter(User.username==userName).first()
        if user is None:
            abort(404)
        return user

    def authenticate(self,userName,password):
        user = self.filter(db.or_(User.username==userName,User.email==userName)).first()
        if user:
            authed = user.check_password(password)
        else:
            authed = False
        return user,authed


class User(db.Model):
    __tablename__ = 'users'
    query_class = UserQuery

    NORMAL,VIP,ADMIN = 100, 200,900 
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100),unique=True,index=True)
    email = db.Column(db.String(200), unique=True, nullable=False, index=True)
    password = db.Column(db.String(100), nullable=False)
    website = db.Column(db.String(400))
    role = db.Column(db.Integer, default=1)
    token = db.Column(db.String(16))
    city = db.Column(db.String(200))
    description = db.Column(db.Text)
    actived = db.Column(db.Boolean,default=False)
    createtime = db.Column(db.DateTime, default=datetime.now)
    last_login = db.Column(db.DateTime, default=datetime.now)

    def __init__(self, email, **kwargs):
        self.email = email.lower()
        
        if 'password' in kwargs:
            raw = kwargs.pop('password')
            self.password = generate_password_hash(raw)
        for k, v in kwargs.items():
            setattr(self, k, v)

    def check_password(self, raw):
        return check_password_hash(self.password, raw)

    @property
    def is_admin(self):
        return self.role>= self.ADMIN

    @property
    def is_vip(self):
        return self.role >= self.VIP

    @cached_property
    def provides(self):
        needs = [UserNeed(self.id),loginNeed]
        if self.is_admin:
            needs.append(adminNeed)
        if self.is_vip:
            needs.append(vipNeed)
        return needs

    @staticmethod
    def create_token(length=16):
        from random import choice
        chars = ('0123456789'
                'abcdefghijklmnopqrstuvwxyz'
                'ABCDEFGHIJKLMNOPQRSTUVWXYZ')
        salt = ''.join([choice(chars) for i in range(length)])
        return salt
