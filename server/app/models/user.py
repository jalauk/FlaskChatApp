from app.models import db
from datetime import datetime

class User(db.Document):
    meta = {"collection":"users"}
    username = db.StringField(required=True,unique=True)
    name = db.StringField()
    email = db.StringField()
    password = db.StringField(required=True)
    profile = db.StringField()
    last_online = db.DateTimeField()
    created_at = db.DateTimeField(default=datetime.now())
    updated_at = db.DateTimeField(default=datetime.now())