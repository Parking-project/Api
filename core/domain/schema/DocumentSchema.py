from marshmallow import fields, Schema

class DocumentSchema(Schema):
    ID = fields.String()
    document_file_id = fields.String()
    document_file_unique_id = fields.String()
    document_file_size = fields.Integer()
    document_file_url = fields.String()
    document_file_mime = fields.String()

    message_id = fields.String()