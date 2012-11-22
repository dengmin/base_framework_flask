#! /usr/bin/env python
#coding=utf-8

from flask import Blueprint
from src.apps.account.models import User

app = Blueprint('dashboard',__name__)



@app.route('/')
def index():
	return 'admin'

@app.route('/article')
def get_articles():
	pass