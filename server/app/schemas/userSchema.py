from marshmallow import fields,Schema
from marshmallow.validate import Length


class SignupSchema(Schema):
    username = fields.Str(required=True,validate=Length(min=3,max=64))
    email = fields.Email(required=True,validate=Length(max=128))
    password = fields.Str(required=True,validate=Length(max=32,min=8))

    class Meta:
        fields = ("email", "password", "username")

signup_schema = SignupSchema()

class LoginSchema(Schema):
    email = fields.Email(required=True,validate=Length(max=128))
    password = fields.Str(required=True,validate=Length(max=32,min=8))

    class Meta:
        fields = ("email", "password")

login_schema = LoginSchema()