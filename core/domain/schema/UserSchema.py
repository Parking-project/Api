from marshmallow import fields, Schema

class UserSchema(Schema):
    ID = fields.String()
    user_login = fields.String()
    user_salt = fields.String()
    user_pass = fields.String()
    user_display_name = fields.String()
    user_registered = fields.Integer()

    role_id = fields.String()
