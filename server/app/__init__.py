import os
from uuid import uuid4
from flask import Flask,request
import app.config as config
from app.Controllers import userController
from app.Controllers import messageController
from app.models import db
from app.models.chat import Chat
from app.models.user import User
from app.models.message import Message
from flask_cors import CORS
from flask_socketio import SocketIO,join_room,leave_room
from redis import Redis
from app.utils.helper import httpResponse
from app.exceptions.accessDeniedException import AccessDeniedException
from app.exceptions.badRequestException import BadRequestException
from app.exceptions.unauthorizedException import UnauthorizedException
from app.exceptions.unprocessableEntityException import UnprocessableEntityException

app = Flask(__name__)
CORS(app, support_credentials=True)

redis_obj = Redis(host='localhost', port=6379, decode_responses=True)

if os.environ.get("APP_ENV") == "dev":
    app.config.from_object(config.DevelopmentConfig)
elif os.environ.get("APP_ENV") == "prod":
    app.config.from_object(config.ProductionConfig)

db.__init__(app)

app.register_blueprint(userController.bp)
app.register_blueprint(messageController.bp)

@app.errorhandler(404)
def err_404(e):
    return httpResponse(404,"Page Not Found!")

@app.errorhandler(405)
def err_405(e):
    return httpResponse(405,"Method Not Allowed!")

@app.errorhandler(UnauthorizedException)
def err_401(e):
    return httpResponse(401,"Unauthorized",e.errors)

@app.errorhandler(AccessDeniedException)
def err_403(e):
    return httpResponse(403,"Access Denied",e.errors)

@app.errorhandler(BadRequestException)
def err_400(e):
    return httpResponse(400,"Bad Request",e.errors)

@app.errorhandler(UnprocessableEntityException)
def err_422(e):
    return httpResponse(422,"Unprocessable Entity",e.errors)

@app.errorhandler(Exception)
def err_500(e):
    print(e)
    return httpResponse(500,"Server Error.")

socketio = SocketIO(app,cors_allowed_origins="*")

ONLINE_USER = {}

@socketio.on("connect")
def connect():
    print("connect")

@socketio.on("add-user")
def addUser(user_id):
    ONLINE_USER[user_id] = False

@socketio.on("create-room")
def createRoom(data):
    room_id = str(uuid4())
    participants = []
    participants.append(data["user_id"])
    participants.append(data["friend_id"])
    chat = Chat(room_id=room_id,participants=participants)
    chat.save()
    return room_id

@socketio.on("join-room")
def joinRoom(data):
    join_room(data["room_id"])
    return True

@socketio.on("send-message")
def sendMessage(data):
    chat_id = Chat.objects(room_id=data["room_id"]).first().id
    try:
        message_obj = Message(chat_id=str(chat_id),sender=data["from"],text=data["message"])
        message_obj.save()
        socketio.emit("receive-message",{"message" : data["message"],"from" : data["from"]},to=data["room_id"])
    except Exception as e:
        raise e
    return data

@socketio.on("is-typing")
def isTyping(data):
    socketio.emit("typing",data,to=data["room_id"])

@socketio.on("leave-room")
def leaveRoom(data):
    print(data)

if __name__ == "__main__":
    socketio.run(app)
