from flask import request,Blueprint
from app.services import userService
from app.utils.helper import httpResponse
from app.middlewares.validationMiddleware import validate
from app.middlewares.authMiddleware import refreshAuth,auth
from app.schemas.userSchema import signup_schema,login_schema

bp = Blueprint("user",__name__,url_prefix="/api/user")

@bp.post("/signup")
@validate(signup_schema)
def signup():
    username = request.json["username"]
    email = request.json["email"]
    password = request.json["password"] 
    data = userService.signup(username,email,password)
    if data:
        return data
    return httpResponse(201,"Success")

@bp.post("/login")
@validate(login_schema)
def login():
    email = request.json["email"]
    password = request.json["password"] 
    return userService.login(email,password)

@bp.get("/reset-token")
@refreshAuth
def resetToken():
    data = userService.resetToken(request.user_id,request.token,)
    return httpResponse(200,"Success",data)

@bp.get("/get-all-users")
@auth
def getAllUsers():
    data = userService.getAllUsers(request.user_id)
    return httpResponse(200,"Success",data)

@bp.get("/get-all-chats")
@auth
def getAllChats():
    data = userService.getAllChats(request.user_id)
    return httpResponse(200,"Success",data)