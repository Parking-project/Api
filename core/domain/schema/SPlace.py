from marshmallow import fields, Schema

class SPlace(Schema):
    ID = fields.String()
    place_is_valid = fields.Boolean()
    place_code = fields.String()