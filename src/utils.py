#! /usr/bin/env python
#coding=utf-8
from flask import g,request
from werkzeug.contrib.cache import SimpleCache
cache = SimpleCache()

def after_this_request(func):
    if not hasattr(g, 'call_after_request'):
        g.call_after_request = []
    g.call_after_request.append(func)
    return func

def import_object(name, arg=None):
    if '.' not in name:
        return __import__(name)
    parts = name.split('.')
    obj = __import__('.'.join(parts[:-1]), None, None, [parts[-1]], 0)
    return getattr(obj, parts[-1], arg)

class ObjectDict(dict):
    def __getattr__(self, key):
        if key in self:
            return self[key]
        return None

    def __setattr__(self, key, value):
        self[key] = value

class cached(object):
    '''cache a single page'''

    def __init__(self,timeout=None):
        self.timeout = timeout or 300

    def __call__(self,f):
        def decorator(*args, **kwargs):
            response = cache.get(request.path)
            if response is None:
                response = f(*args, **kwargs)
                cache.set(request.path, response, self.timeout)
            return response
        return decorator
