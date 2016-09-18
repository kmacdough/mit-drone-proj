from flask import jsonify
from functools import wraps


def error_handle(fn):
    @wraps(fn)
    def decorated(*args, **kwargs):
        try:
            return fn(*args, **kwargs)
        except Exception as e:
            try:
                return jsonify(status='error', message=e.message)
            except:
                return jsonify(status='error', message='')
    return decorated
