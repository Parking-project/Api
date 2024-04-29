from marshmallow import fields, Schema

class AuthHistorySchema(Schema):
    ID = fields.String()
    auth_date = fields.Integer()
    user_id = fields.String()

