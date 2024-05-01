from marshmallow import fields, Schema

class SRole(Schema):
    ID = fields.String()
    role_name = fields.String()
