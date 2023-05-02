from datetime import datetime
from werkzeug.security import generate_password_hash,check_password_hash
from app.models.user import User
import json 
from app.models.chat import Chat
from app.models.refresh_token import RefreshToken
from app.utils.helper import httpResponse
from app.utils.helper import generateAccessToken,generateRefreshToken

def signup(username,email,password):
    user = User.objects(username=username)
    if user:
        return httpResponse(310,"Already Exsits",{"message":"Duplicate username"})
    user = User.objects(email=email)
    if user:
        return httpResponse(310,"Already Exsits",{"message":"Duplicate Email"})
    password = str(generate_password_hash(password))
    try:
        user = User(username=username,email=email,password=password)
        user.save()
    except Exception as e:
        raise e

def login(email,password):
    try:
        user = User.objects(email=email)
        if not user:
            return httpResponse(301,"No Record Found",{"message":"User Doesn't Exist."})
        if not check_password_hash(user[0].password,password):
            return httpResponse(302,"Invalid Credential",{"message":"Invalid Credentials"})
        
        access_token = generateAccessToken(str(user[0].id))
        refresh_token = generateRefreshToken(str(user[0].id))

        refresh_token = RefreshToken(user_id=user[0].id,refresh_token=refresh_token)
        refresh_token.save()
        
        user = user[0].to_json()
        user = json.loads(user)
        return httpResponse(200,"Success",{
            "tokens" : {
                "access_token":access_token,
                "refresh_token":refresh_token.refresh_token
            },
            "user" : {
                "username" : user["username"],
                "_id": user["_id"]
            }
        })

    except Exception as e:
        print("error : ",e)

def resetToken(user_id,token):
    try:
        refresh_token_obj = RefreshToken.objects(refresh_token=token)
        if refresh_token_obj:
            access_token = generateAccessToken(user_id)
            refresh_token = generateRefreshToken(user_id)
            refresh_token_obj.update_one(set__refresh_token = refresh_token,set__updated_at = datetime.now())
            return {"tokens" : {
                                "access_token":access_token,
                                "refresh_token":refresh_token
                                },
                    }
        return {}
    except Exception as e:
        print(e.args)
        raise Exception(e)
    
def getAllUsers(user_id):
    chats = Chat.objects(participants=user_id).only("participants").exclude("id")
    chats = chats.to_json()
    chats = json.loads(chats)

    #to remove existing chats
    chat_list = []
    for chat in chats:
        for participant in chat["participants"]:
            if participant["$oid"] != user_id:
                chat_list.append(participant["$oid"])
    chat_list.append(user_id)


    users = User.objects.filter(id__nin=chat_list)   
    users = users.to_json()
    users = json.loads(users)
    for user in users:
        for key in list(user.keys()):
            if key not in ["_id","username"]:
                del user[key]
    return users

def getAllChats(user_id):
    chats = Chat.objects(participants=user_id).all()
    chat_list = []
    for chat in chats:
        current_chat = {}
        current_chat["room_id"] = chat.room_id
        for participant in chat.participants:
            if user_id != str(participant.id):
                current_chat["_id"] = {"$oid" : str(participant.id)}
                current_chat["username"] = participant.username
        chat_list.append(current_chat)
    return chat_list
