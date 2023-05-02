from app.models import db
from app.models.user import User
from app.models.chat import Chat
from datetime import datetime

class Message(db.Document):
    meta = {"collection":"messages"}
    chat_id = db.ReferenceField(Chat)
    text = db.StringField(required=True)
    seen_by = db.ListField()
    sender = db.ReferenceField(User)
    # reply_to = db.RefrenceField(Message)
    created_at = db.DateTimeField(default=datetime.now())
    updated_at = db.DateTimeField(default=datetime.now())