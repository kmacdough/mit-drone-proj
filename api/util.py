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


def rename(newname):
    def decorator(f):
        f.__name__ = newname
        return f
    return decorator

def expand_ref(dct, id_field, expanded_field, cls, db):
    obj_id = dct[id_field]
    obj = cls.get_by_id(obj_id)
    obj_dict = obj.to_dict(expand_refs=True, db=db)

    del dct[id_field]
    dct[expanded_field] = obj_dict