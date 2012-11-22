#! /usr/bin/env python
#coding=utf-8


from flask import Blueprint,render_template
from src.utils import cached
app = Blueprint('front',__name__)

@app.route('/')
@cached(timeout=20)
def index():
	print 'index'
	return render_template('index.html',gender='M')


@app.route('/about')
def about():
	return 'about'