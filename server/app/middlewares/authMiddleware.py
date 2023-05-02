from functools import wraps
from flask import request
import jwt
from app.config import Config
from app.exceptions.unauthorizedException import UnauthorizedException
from app.exceptions.accessDeniedException import AccessDeniedException

def auth(f):
    @wraps(f)
    def wrapper(*args,**kwargs):
        token = None
        if "Authorization" in request.headers:
            token = request.headers["Authorization"]
            token = token.replace("Bearer ","")
            try:
                data = jwt.decode(token,Config.ACCESS_TOKEN_SECRET_KEY,algorithms=["HS256"])
                if data:
                    request.user_id = data["id"]
                    return f(*args,**kwargs)
                else:
                    raise AccessDeniedException({})
            except jwt.ExpiredSignatureError :
                raise UnauthorizedException({})
            except jwt.InvalidTokenError:
                raise UnauthorizedException({})
            except Exception as e: 
                raise e
        raise UnauthorizedException({})
    return wrapper


def refreshAuth(f):
    @wraps(f)
    def wrapper(*args,**kwargs):
        token = None
        if "Authorization" in request.headers:
            token = request.headers["Authorization"]
            token = token.replace("Bearer ","")
            try:
                data = jwt.decode(token,Config.REFRESH_TOKEN_SECRET_KEY,algorithms=["HS256"])
                if data:
                    request.user_id = data["id"]
                    request.token = token
                    return f(*args,**kwargs)
                else:
                    raise AccessDeniedException({})
            except jwt.ExpiredSignatureError :
                raise UnauthorizedException({})
            except jwt.InvalidTokenError:
                raise UnauthorizedException({})
            except Exception as e: 
                raise e
        raise UnauthorizedException({})
    return wrapper