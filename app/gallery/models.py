from marshmallow_jsonapi import Schema, fields
from marshmallow import validate
from app.basemodels import db, CRUD_MixIn


class Gallery(db.Model, CRUD_MixIn):
    id = db.Column(db.Integer, primary_key=True)

    name = db.Column(db.String(250), nullable=False)
    tags = db.Column(db.Text, nullable=False)
    path = db.Column(db.Text, nullable=False)
    creation_date = db.Column(
        db.TIMESTAMP, server_default=db.func.current_timestamp(), nullable=False)
    category = db.Column(db.String(250), nullable=False)

    def __init__(self,  name,  tags,  path, category):

        self.name = name
        self.tags = tags
        self.path = path
        self.category = category


class GallerySchema(Schema):

    not_blank = validate.Length(min=1, error='Field cannot be blank')
    # add validate=not_blank in required fields
    id = fields.Integer(dump_only=True)

    name = fields.String(validate=not_blank)
    tags = fields.String(validate=not_blank)
    path = fields.String(validate=not_blank)
    creation_date = fields.DateTime(dump_only=True)
    category = fields.String(validate=not_blank)

    # self links
    def get_top_level_links(self, data, many):
        if many:
            self_link = "/gallery/"
        else:
            self_link = "/gallery/{}".format(data['id'])
        return {'self': self_link}

    class Meta:
        type_ = 'files'
