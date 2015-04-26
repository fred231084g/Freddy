from app import db
from flask.ext.login import LoginManager, login_user,UserMixin, logout_user
from sqlalchemy.sql.expression import text
from sqlalchemy.exc import SQLAlchemyError


class Users(db.Model, UserMixin):
  id = db.Column(db.Integer, primary_key=True)
  email = db.Column(db.String(250), unique=True, nullable=False)
  password = db.Column(db.String(250), nullable=False)
  name = db.Column(db.String(250), nullable=False)
  created_on = db.Column(db.TIMESTAMP,server_default=db.func.current_timestamp(),nullable=False)
  #User is active if status is 0
  status = db.Column(db.Integer(), server_default='0', nullable=False)
  activation_key=db.Column(db.String(255))
  posts = db.relationship('Post', backref='user')


  def __init__(self,email,password,name):
    self.email=email
    self.password=password
    self.name=name

  def get_id(self):
    return str(self.id)

  def add(self,user):
     db.session.add(user)
     return session_commit ()

  def update(self):
      return session_commit()

  def delete(self,user):
     db.session.delete(user)
     return session_commit()


term_relationships=db.Table('term_relationships',db.Column('id', db.Integer, primary_key=True),  db.Column('post_id', db.Integer,db.ForeignKey('post.id'), nullable=False),
                             db.Column('term_id',db.Integer,db.ForeignKey('terms.id'),nullable=False))

class TermRelationships():
    def __init__(self,post_id,term_id):
      self.post_id=post_id
      self.term_id=term_id

db.mapper(TermRelationships, term_relationships)

#make table name plural
class Post(db.Model):
  id = db.Column(db.Integer, primary_key=True)
  author = db.Column(db.Integer, db.ForeignKey('users.id'))
  title = db.Column(db.String(255),nullable=False)
  slug = db.Column(db.String(255), nullable=False)
  #Remove created_on and make default like wordpress
  date=db.Column(db.TIMESTAMP,server_default='0000-00-00 00:00:00', nullable=False)
  created_on=db.Column(db.TIMESTAMP,server_default=db.func.current_timestamp(), nullable=False)
  content = db.Column(db.Text)
  #Remove publish, status will replace publish
  published = db.Column(db.Boolean, default=True, nullable=False)
  status = db.Column(db.String(20), server_default='publish', nullable=False)
  #Need to make not null
  modified = db.Column(db.TIMESTAMP,server_default=db.func.current_timestamp(),nullable=False)
  post_type=db.Column(db.String(20), server_default='post', nullable=False)
  terms=db.relationship('Terms', secondary=term_relationships, backref='posts')
  comments = db.relationship('Comment', backref="post", cascade="all, delete-orphan" , lazy='dynamic')


  def __init__(self, author,title,slug, content,status,post_type):
        self.author = author
        self.title = title
        self.slug = slug
        self.content = content
        self.status = status
        self.post_type = post_type


  def add(self,post):
      db.session.add(post)
      return session_commit()

  def update(self):
      return session_commit()

  def delete(self,post):
     db.session.delete(post)
     return session_commit()

class PostMeta(db.Model):
  id = db.Column(db.Integer, primary_key=True)
  post_id=db.Column(db.Integer,db.ForeignKey('post.id'))
  key=db.Column(db.String(255))
  value=db.Column(db.Text)

  def __init__(self, post_id,key,value):
        self.post_id = post_id
        self.key = key
        self.value = value

  def add(self,post_meta):
      db.session.add(post_meta)
      return session_commit()

  def update(self):
      return session_commit()

  def delete(self,post):
     db.session.delete(post)
     return session_commit()

class Terms(db.Model):
     id=db.Column(db.Integer, primary_key=True)
     name=db.Column(db.String, unique=True, nullable=False)
     #Make nullable=False
     slug = db.Column(db.String(255), nullable=False)
     description=db.Column(db.Text)
     taxonomy=db.Column(db.Enum('category', 'tag', name='taxonomy'), nullable=False)
     parent=db.Column(db.Integer, server_default=None, nullable=False)


     def __init__(self,name,slug,description,taxonomy,parent):
        self.name=name
        self.slug=slug
        self.description=description
        self.taxonomy=taxonomy
        self.parent=parent

     def add(self,term):
         db.session.add(term)
         return session_commit()

     def update(self):
      return session_commit()

     def delete(self,term):
         db.session.delete(term)
         return session_commit()




class Comment(db.Model):
  id = db.Column(db.Integer, primary_key=True)
  author = db.Column(db.String(128),nullable=False)
  created_on = db.Column(db.TIMESTAMP,server_default=db.func.current_timestamp(),nullable=False)
  website = db.Column(db.String(255))
  content = db.Column(db.Text, nullable=False)
  approved = db.Column(db.Boolean, default=1)
  post_id = db.Column(db.Integer, db.ForeignKey('post.id'))

  def __init__(self, author,website, content,post_id,approved):
        self.author = author
        self.website = website
        self.content=content
        self.approved=approved
        self.post_id=post_id

  def get_id(self):
    return unicode(self.id)

  def add(self, comment):
      db.session.add(comment)
      return session_commit()

  def update(self):
      return session_commit()

  def delete(self,comment):
     db.session.delete(comment)
     return session_commit()



#Universal functions

def  session_commit ():
      try:
        db.session.commit()
      except SQLAlchemyError as e:
         reason=str(e)
         return reason
