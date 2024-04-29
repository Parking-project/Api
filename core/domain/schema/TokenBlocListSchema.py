from marshmallow import fields, Schema

class TokenBlocListSchema(Schema):
    ID = fields.String()
    token_jti = fields.String()
    token_create = fields.Integer()
