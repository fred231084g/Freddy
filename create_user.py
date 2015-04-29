from app.models import Users
from app import db
from werkzeug.security import generate_password_hash
from sqlalchemy.exc import SQLAlchemyError

name='Leo'
email='leo@leog.in'
password=generate_password_hash('password')
user=Users(email,password,name)
db.session.add(user)


try:
  db.session.commit()
  print("{} was added successfully".format(email))
except SQLAlchemyError as e:
  reason=str(e)
  print (reason)
