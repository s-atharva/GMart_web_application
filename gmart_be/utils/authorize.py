from flask_jwt_extended import get_jwt_identity
from flask_jwt_extended import get_jwt
from functools import wraps
from flask import jsonify


def role_required(roles):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            current_user = get_jwt_identity()
            user_claims = get_jwt()

            if user_claims.get('role') in roles:
                return func(*args, **kwargs)
            else:
                return jsonify(message='You do not have access to this resource.'), 403

        return wrapper
    return decorator
