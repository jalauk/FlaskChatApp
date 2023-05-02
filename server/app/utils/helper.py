from datetime import datetime,timedelta
import jwt
from app.config import Config

def httpResponse(code,message,data={}):
    status = True if code>=200 and code<=299 else False
    return {
        "code" : code,
        "status" : status,
        "message" : message,
        "data" : data
    }

def generateToken(id:str,seconds:int,SECRET_KEY):
    payload = {
        'id' : id,
        'exp' : datetime.utcnow() + timedelta(seconds=seconds),
        'iat' : datetime.utcnow()
    }
    return jwt.encode(
        payload,
        SECRET_KEY,
        algorithm='HS256'
    )

def generateAccessToken(id:str):
    return generateToken(id,int(Config.ACCESS_TOKEN_EXP_TIME),Config.ACCESS_TOKEN_SECRET_KEY)

def generateRefreshToken(id:str):
    return generateToken(id,int(Config.REFRESH_TOKEN_EXP_TIME),Config.REFRESH_TOKEN_SECRET_KEY)
