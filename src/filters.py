#! /usr/bin/env python
#coding=utf-8

from datetime import datetime
from flask import request,render_template,jsonify

def register_template_filters(app):
    @app.template_filter()
    def sex(value):
        r = u'保密'
        if value=='F':
            r = u"女"
        elif value=='M':
            r = u"男"
        return r

    @app.template_filter()
    def timesince(dt, default=None):
        
        if default is None:
            default = u"刚才"

        now = datetime.now()
        diff = now - dt

        years = diff.days / 365
        months = diff.days / 30
        weeks = diff.days / 7
        days = diff.days
        hours = diff.seconds / 3600
        minutes = diff.seconds / 60
        seconds = diff.seconds 

        periods = (
            (years, u"%(num)s 年" % dict(num=years)),
            (months, u"%(num)s 月" % dict(num=months)),
            (weeks, u"%(num)s 周" % dict(num=weeks)),
            (days, u"%(num)s 天" % dict(num=days)),
            (hours, u"%(num)s 小时" % dict(num=hours)),
            (minutes, u"%(num)s 分钟" % dict(num=minutes)),
            (seconds, u"%(num)s 秒" % dict(num=seconds)),
        )

        for period, trans in periods:
            if period:
                return u"%(period)s前" % dict(period=trans)

        return default

    @app.template_filter()
    def datesince(dt):
        if not dt:
            return ''
        now = datetime.now()
        ms = '%s %d:%02d'
        if dt.day == now.day-1 and dt.month == now.month and dt.year == now.year:
            ms = ms % (u'昨天', dt.hour, dt.minute)
        elif dt.day == now.day-2  and dt.month == now.month and dt.year == now.year:
            ms = ms % (u'前天', dt.hour, dt.minute)
        elif dt.day == now.day  and dt.month == now.month and dt.year == now.year:
            ms = ms % (u'今天', dt.hour, dt.minute)
        else:
            ms = ms % (str(dt.date()), dt.hour, dt.minute)
        return ms


def error_handers(app):

    @app.errorhandler(401)
    def unauthorized(error):
        if request.is_xhr:
            return jsonify(success=False, error=u"请先登录", login=True, next=request.url)
        return render_template('error/401.html',error=error)

    @app.errorhandler(403)
    def forbidden(error):
        if request.is_xhr:
            return jsonify(success=False,error=error)
        return render_template('error/403.html',error=error)

    @app.errorhandler(404)
    def page_not_found(error):
        if request.is_xhr:
            return json.dumps(success=False,error='页面未找到')
        return render_template('errors/404.html',error=error)
    
    @app.errorhandler(413)
    def request_entity_too_large(error):
        if request.is_xhr:
            return jsonify(success=False,error='Request Entity too Large')
        return render_template('errors/404.html',error=error)
    
    @app.errorhandler(500)
    def server_error(error):
        if request.is_xhr:
            return jsonify(error=u'服务器内部错误',success=False)
        return render_template('errors/500.html',error=error)