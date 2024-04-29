from marshmallow import fields, Schema

class RoleSchema(Schema):
    ID = fields.String()
    role_name = fields.String()
