from marshmallow import fields, Schema

class SAuthHistory(Schema):
    ID = fields.String()
    auth_date = fields.Integer()
    user_id = fields.String()
