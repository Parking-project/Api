from marshmallow import fields, Schema

class UserMetaSchema(Schema):
    ID = fields.String()
    user_meta_key = fields.String()
    user_meta_value = fields.String()

    user_id = fields.String()
    