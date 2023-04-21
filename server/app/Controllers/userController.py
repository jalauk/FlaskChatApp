from flask import request,Blueprint

bp = Blueprint("user",__name__,url_prefix="/api/user")

@bp.post("/signup")
def signup():
    username = request.json["username"]
    email = request.json["email"]
    password = request.json["password"] 
    return {}