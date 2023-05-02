from app.models.message import Message
from app.models.chat import Chat

def getAllMessage(room_id):
    chat_id = Chat.objects(room_id=room_id).first().id
    print("chat_id : ",chat_id)
    messages = Message.objects(chat_id = chat_id).only("text","sender","created_at").exclude("id")
    message_list = []
    for message in messages:
        message_dict = {}
        message_dict["message"] = message.text
        message_dict["from"] = str(message.sender.id)
        message_dict["time"] = (message.created_at).strftime("%H:%M:%S")
        message_dict["date"] = (message.created_at).strftime("%d/%m/%Y")
        message_list.append(message_dict)
    return message_list
