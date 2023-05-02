from app.models import db
from app.models.user import User
from datetime import datetime

class Chat(db.Document):
    meta = {"collection":"chats"}
    room_id = db.UUIDField(required=True,binary=False)
    participants = db.ListField(db.ReferenceField(User))
    is_group = db.BooleanField(default=False)
    group_name = db.StringField()
    created_at = db.DateTimeField(default=datetime.now())
    updated_at = db.DateTimeField(default=datetime.now())