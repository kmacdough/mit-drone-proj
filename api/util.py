from flask import jsonify
from functools import wraps


def error_handle(fn):
    @wraps(fn)
    def decorated(*args, **kwargs):
        try:
            return fn(*args, **kwargs)
        except Exception as e:
            if hasattr(e, 'message'):
                return jsonify(status='error', message=e.message)
            else:
                return jsonify(status='error', message='')
    return decorated
