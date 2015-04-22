from app import db
from flask.ext.login import LoginManager, login_user,UserMixin, logout_user
from sqlalchemy.sql.expression import text
from sqlalchemy.exc import SQLAlchemyError

class Post(db.Model):
  id = db.Column(db.Integer, primary_key=True)
  author = db.Column(db.String(255))
  title = db.Column(db.String(255),nullable=False)
  slug = db.Column(db.String(255))
  created_on=db.Column(db.TIMESTAMP,server_default=db.func.current_timestamp())
  content = db.Column(db.Text)
  published = db.Column(db.Boolean, default=1, nullable=False)
  #add ondelete manually in alembic
  category = db.Column(db.Integer, db.ForeignKey('terms.id', ondelete="CASCADE"))
  comments = db.relationship('Comment', backref="post", cascade="all, delete-orphan" , lazy='dynamic')

  def __init__(self, author,title,slug, content,published,category):
        self.author = author
        self.title = title
        self.slug = slug
        self.content=content
        self.published=published
        self.category=category

  def get_id(self):
    return str(self.id)

  def add(self,post):
      db.session.add(post)
      return session_commit()

  def update(self):
      return session_commit()

  def delete(self,post):
     db.session.delete(post)
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


class Users(db.Model, UserMixin):
  id = db.Column(db.Integer, primary_key=True)
  email = db.Column(db.String(250), unique=True, nullable=False)
  password = db.Column(db.String(250), nullable=False)
  name = db.Column(db.String(250), nullable=False)
  created_on = db.Column(db.TIMESTAMP,server_default=db.func.current_timestamp(),nullable=False)


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

class Terms(db.Model):
     id=db.Column(db.Integer, primary_key=True)
     name=db.Column(db.String, unique=True, nullable=False)
     description=db.Column(db.String)
     group=db.Column(db.String, nullable=False, server_default='category')

     def __init__(self,name,description):
        self.name=name
        self.description=description

     def add(self,term):
         db.session.add(term)
         return session_commit()

     def update(self):
      return session_commit()

     def delete(self,term):
         db.session.delete(term)
         return session_commit()



#Universal functions

def  session_commit ():
      try:
        db.session.commit()
      except SQLAlchemyError as e:
         reason=str(e)
         return reason
