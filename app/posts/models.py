from marshmallow_jsonapi import Schema, fields
from marshmallow import validate
from app.basemodels import db, CRUD_MixIn
from app.terms.models import TermsSchema

# Many to Many Relationships with Posts and terms

term_relationships=db.Table('term_relationships',

                             db.Column('post_id', db.Integer,db.ForeignKey('posts.id'), nullable=False),
                             db.Column('term_id',db.Integer,db.ForeignKey('terms.id'),nullable=False),
                             db.PrimaryKeyConstraint('post_id', 'term_id')
                             )

class TermRelationships():
    def __init__(self,post_id,term_id):
      self.post_id=post_id
      self.term_id=term_id

db.mapper(TermRelationships, term_relationships)

class Posts(db.Model, CRUD_MixIn):
    id = db.Column(db.Integer, primary_key=True)
    author = db.Column(db.String(250), nullable=False)
    title = db.Column(db.Text, nullable=False)
    slug = db.Column(db.String(250), nullable=False)
    date = db.Column(
        db.TIMESTAMP, server_default=db.func.current_timestamp(), nullable=False)
    date_gmt = db.Column(
        db.TIMESTAMP, server_default=db.func.current_timestamp(), nullable=False)
    content = db.Column(db.Text, nullable=False)
    excerpt = db.Column(db.Text, nullable=False)
    status = db.Column(db.String(250), server_default='publish', nullable=False)
    modified = db.Column(
        db.TIMESTAMP, server_default=db.func.current_timestamp(), nullable=False)
    modified_gmt = db.Column(
        db.TIMESTAMP, server_default=db.func.current_timestamp(), nullable=False)
    type = db.Column(db.String(250), server_default='post', nullable=False)
    parent = db.Column(db.Integer, nullable=False)
    #featured Image Path
    path = db.Column(db.Text)
    terms = db.relationship('Terms', secondary=term_relationships, backref='posts' )
    comments = db.relationship('Comments', backref="post", cascade="all, delete-orphan" , lazy='dynamic')

    def __init__(self,  author,  title,  slug,  content,  excerpt,  status,  type,  parent, path):

        self.author = author
        self.title = title
        self.slug = slug
        self.content = content
        self.excerpt = excerpt
        self.status = status
        self.type = type
        self.parent = parent
        self.path = path

class PostsSchema(Schema):

    not_blank = validate.Length(min=1, error='Field cannot be blank')
    # add validate=not_blank in required fields
    id = fields.Integer(dump_only=True)

    author = fields.String(validate=not_blank)
    title = fields.String(validate=not_blank)
    slug = fields.String(validate=not_blank)
    content = fields.String(validate=not_blank)
    date = fields.String(dump_only=True)
    modified = fields.String(dump_only=True)
    excerpt = fields.String(validate=not_blank)
    status = fields.String(validate=not_blank)
    type = fields.String(validate=not_blank)
    path = fields.String()
    parent = fields.Integer(required=True)
    terms  = fields.Nested(TermsSchema, many=True)
    #term_ids = fields.List(fields.Integer())
    term_ids = fields.Raw()

    # self links
    def get_top_level_links(self, data, many):
        if many:
            self_link = "/posts/"
        else:
            self_link = "/posts/{}".format(data['id'])
        return {'self': self_link}

    class Meta:
        type_ = 'posts'
