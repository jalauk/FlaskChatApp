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
from app.utils.helper import httpResponse
from app.exceptions.accessDeniedException import AccessDeniedException
from app.exceptions.badRequestException import BadRequestException
from app.exceptions.unauthorizedException import UnauthorizedException
from app.exceptions.unprocessableEntityException import UnprocessableEntityException
from datetime import datetime
from app.models import r

app = Flask(__name__)
CORS(app, support_credentials=True)

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

@socketio.on("connect")
def connect():
    print("connect")

@socketio.on("add-user")
def addUser(user_id):
    r.set(user_id,request.sid)
    
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
        message_obj = Message(chat_id=str(chat_id),sender=data["from"],text=data["message"],created_at=datetime.now())
        message_obj.save()
        socketio.emit("receive-message",{"message" : data["message"],"from" : data["from"],"time":str(datetime.now().strftime("%H:%M:%S"))},to=data["room_id"])
    except Exception as e:
        raise e
    return data

@socketio.on("is-typing")
def isTyping(data):
    socketio.emit("typing",data,to=data["room_id"])

@socketio.on("leave-room")
def leaveRoom(data):
    leave_room(data["room_id"])
    # return ONLINE_USER

@socketio.on("disconnect")
def disconnectEvent():
    # for key, value in ONLINE_USER.items():
    #     if request.sid == value:
    #         user_id = key

    # del ONLINE_USER[user_id]

    try:
        User.objects(id=user_id).update_one(set__last_online=datetime.now())
    except Exception as e:
        print(e)

if __name__ == "__main__":
    socketio.run(app)
