from marshmallow import fields, Schema

class MessageSchema(Schema):
    ID = fields.String()
    message_date = fields.Integer()
    message_text = fields.String()
    message_iterator = fields.Integer()

    user_id = fields.String()
    message_root_id = fields.String()
    message_answer_id = fields.String()
