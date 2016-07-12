from marshmallow_jsonapi import Schema, fields
from marshmallow import validate
from app.basemodels import db, CRUD_MixIn


class Terms(db.Model, CRUD_MixIn):

    __table_args__ = (db.UniqueConstraint('name', 'taxonomy'),)    
    id = db.Column(db.Integer, primary_key=True)    
    name = db.Column(db.String(250), nullable=False)
    slug = db.Column(db.String(250), nullable=False)
    description = db.Column(db.Text)
    taxonomy = db.Column(db.String(250), nullable=False)
    parent = db.Column(db.Integer, server_default=None, nullable=False)

    def __init__(self,  name,  slug,  description,  taxonomy,  parent, ):

        self.name = name
        self.slug = slug
        self.description = description
        self.taxonomy = taxonomy
        self.parent = parent


class TermsSchema(Schema):

    not_blank = validate.Length(min=1, error='Field cannot be blank')
    # add validate=not_blank in required fields
    id = fields.Integer(dump_only=True)

    name = fields.String(validate=not_blank)
    slug = fields.String(validate=not_blank)
    description = fields.String(validate=not_blank)
    taxonomy = fields.String(validate=not_blank)
    parent = fields.Integer(required=True)

    # self links
    def get_top_level_links(self, data, many):
        if many:
            self_link = "/terms/"
        else:
            self_link = "/terms/{}".format(data['id'])
        return {'self': self_link}

    class Meta:
        type_ = 'terms'
