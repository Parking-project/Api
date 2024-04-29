from marshmallow import fields, Schema

class MessageMetaSchema(Schema):
    ID = fields.String()
    message_meta_key = fields.String()
    message_meta_value = fields.String()

    message_id = fields.String()