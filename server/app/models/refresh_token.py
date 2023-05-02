from app.models import db
from datetime import datetime
from app.models.user import User

class RefreshToken(db.Document):
    meta = {'collection': 'refresh_tokens'}
    user_id = db.ReferenceField(User)
    refresh_token = db.StringField(required=True)
    created_at = db.DateTimeField(required=True,default=datetime.now())
    updated_at = db.DateTimeField(required=True,default=datetime.now())