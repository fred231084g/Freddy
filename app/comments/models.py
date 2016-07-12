from marshmallow_jsonapi import Schema, fields
from marshmallow import validate
from app.basemodels import db, CRUD_MixIn


class Comments(db.Model, CRUD_MixIn):
    id = db.Column(db.Integer, primary_key=True)
    post_id = db.Column(db.Integer, db.ForeignKey('posts.id'), nullable=False)
    author_name = db.Column(db.String(250), nullable=False)
    author_email = db.Column(db.String(250), nullable=False)
    author_url = db.Column(db.Text)
    created_on = db.Column(
        db.TIMESTAMP, server_default=db.func.current_timestamp(), nullable=False)
    content = db.Column(db.Text, nullable=False)
    karma = db.Column(db.Integer, default = 0 )
    approved = db.Column(db.String(250), nullable=False)
    agent = db.Column(db.Text)
    type = db.Column(db.String(250))
    parent = db.Column(db.Integer,  default = 0, nullable=False)

    def __init__(self,  post_id,  author_name,  author_email,  author_url,  created_on,  content,  karma,  approved,  agent,  type,  parent, ):

        self.post_id = post_id
        self.author_name = author_name
        self.author_email = author_email
        self.author_url = author_url
        self.created_on = created_on
        self.content = content
        self.karma = karma
        self.approved = approved
        self.agent = agent
        self.type = type
        self.parent = parent


class CommentsSchema(Schema):

    not_blank = validate.Length(min=1, error='Field cannot be blank')
    # add validate=not_blank in required fields
    id = fields.Integer(dump_only=True)

    post_id = fields.Integer(required=True)
    author_name = fields.String(validate=not_blank)
    author_email = fields.String(validate=not_blank)
    author_url = fields.String(validate=not_blank)
    created_on = fields.DateTime(required=True)
    content = fields.String(validate=not_blank)
    karma = fields.Integer(required=True)
    approved = fields.String(validate=not_blank)
    agent = fields.String(validate=not_blank)
    type = fields.String(validate=not_blank)
    parent = fields.Integer(required=True)

    # self links
    def get_top_level_links(self, data, many):
        if many:
            self_link = "/comments/"
        else:
            self_link = "/comments/{}".format(data['id'])
        return {'self': self_link}

    class Meta:
        type_ = 'comments'
