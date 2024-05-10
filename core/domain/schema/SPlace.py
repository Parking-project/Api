from marshmallow import fields, Schema

class SPlace(Schema):
    ID = fields.String()
    place_code = fields.String()
