from marshmallow import fields, Schema

class SReserveHistory(Schema):
    ID = fields.String()
    reserve_id = fields.String()
    reserve_state = fields.Integer()
