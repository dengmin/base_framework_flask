#! /usr/bin/env python
#coding=utf-8

from flask.ext.wtf import Form,TextField,PasswordField,BooleanField, \
	HiddenField,SubmitField,required

class LoginForm(Form):
	username = TextField('Username/Email',validators=[required(message='You must provide an email or username')])
	password = PasswordField('password')
	remember = BooleanField('remember me')
	next = HiddenField()
	submit = SubmitField('Login')

