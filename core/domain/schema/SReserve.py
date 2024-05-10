from marshmallow import fields, Schema

class SReserve(Schema):
    ID = fields.String(required=True)
    reserve_begin = fields.Integer(required=True)
    reserve_end = fields.Integer(required=True)
    
    place_code = fields.String(required=False)
