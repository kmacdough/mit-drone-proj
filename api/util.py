from flask import jsonify
from functools import wraps

import app

logger = app.logger.getChild(__name__)

def error_handle(fn):
    @wraps(fn)
    def decorated(*args, **kwargs):
        try:
            return fn(*args, **kwargs)
        except Exception as e:
            logger.exception(e)
            if hasattr(e, 'message'):
                return jsonify(status='error', message=e.message)
            else:
                return jsonify(status='error', message='')
    return decorated
