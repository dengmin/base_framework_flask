#! /usr/bin/env python
#coding=utf-8

from flask_principal import RoleNeed, Permission

adminNeed = RoleNeed('admin')
vipNeed = RoleNeed('vip')
loginNeed = RoleNeed('login')

admin = Permission(adminNeed)
vip = Permission(vipNeed)
login = Permission(loginNeed)