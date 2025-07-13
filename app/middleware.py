from flask import jsonify
from functools import wraps
from flask_jwt_extended import jwt_required, get_jwt, verify_jwt_in_request

def role_required(*roles):
    def wrapper(fn):
        @wraps(fn)
        def decorator(*args, **kwargs):
            verify_jwt_in_request()
            claims = get_jwt()

            user_role = claims.get('role')
            if user_role not in roles:
                return jsonify({
                    'status': 'error',
                    'message': f'Akses ditolak. Role harus salah satu dari: {roles}'
                }), 403

            return fn(*args, **kwargs)
        return decorator
    return wrapper