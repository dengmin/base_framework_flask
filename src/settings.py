#! /usr/bin/env python
#coding=utf-8

import os

DEBUG = False

UPLOADS_DEFAULT_DEST = os.path.join(os.path.dirname(__file__),'static/uploads')

UPLOADS_DEFAULT_URL = '/static'

SECRET_KEY = os.urandom(32).encode('hex')

SQLALCHEMY_DATABASE_URI = 'mysql://root:root@localhost:3306/yomo?charset=utf8'
SQLALCHEMY_ECHO = False
SQLALCHEMY_POOL_SIZE = 20

PASSWORD_SECRET = 'sha1'

LOGGER_NAME = 'yormo'
