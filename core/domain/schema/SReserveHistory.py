from marshmallow import fields, Schema

class SReserveHistory(Schema):
    ID = fields.String()
    reserve_id = fields.String()
    reserve_state = fields.Integer()

    reserve_begin = fields.Integer()
    reserve_end = fields.Integer()

    place_code = fields.String()
