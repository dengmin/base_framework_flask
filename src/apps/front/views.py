#! /usr/bin/env python
#coding=utf-8


from flask import Blueprint,render_template
from src.utils import cached
from src.core.permission import login

app = Blueprint('front',__name__)

@app.route('/')
def index():
	return render_template('index.html',gender='M')


@app.route('/about')
@login.require(403)
def about():
	return 'about'