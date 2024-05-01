from marshmallow import fields, Schema

class SReserve(Schema):
    ID = fields.String()
    reserve_begin = fields.Integer()
    reserve_end = fields.Integer()
    reserve_state = fields.Integer()

    place_id = fields.String()
    user_id = fields.String()
