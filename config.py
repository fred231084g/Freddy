import os

# DATABASE SETTINGS
pg_db_username = 'nuxkdhzxuvlkbx'
pg_db_password = 'os.environ['PG_DB_PASSWORD']'
pg_db_name = ''
pg_db_hostname = 'ec2-54-243-249-159.compute-1.amazonaws.com'

# MYSQL
mysql_db_username = 'root'
mysql_db_password = ''
mysql_db_name = 'fscaffold'
mysql_db_hostname = 'localhost'

DEBUG = True
PORT = 5000
HOST = "0.0.0.0"
SQLALCHEMY_ECHO = False
SECRET_KEY = "SOME SECRET"

#Folder to upload files must be inside the templates folder

UPLOAD_FOLDER = "static/files/"

# PostgreSQL
SQLALCHEMY_DATABASE_URI = "postgresql://{DB_USER}:{DB_PASS}@{DB_ADDR}/{DB_NAME}".format(DB_USER=pg_db_username,
                                                                                        DB_PASS=pg_db_password,
                                                                                        DB_ADDR=pg_db_hostname,
                                                                                        DB_NAME=pg_db_name)

# MySQL
"""SQLALCHEMY_DATABASE_URI = "mysql+pymysql://{DB_USER}:{DB_PASS}@{DB_ADDR}/{DB_NAME}".format(DB_USER=mysql_db_username,
                                                                                        DB_PASS=mysql_db_password,
                                                                                        DB_ADDR=mysql_db_hostname,
                                                                                        DB_NAME=mysql_db_name)"""
# Email Server Configuration

MAIL_DEFAULT_SENDER = "leo@localhost"

PASSWORD_RESET_EMAIL ="""
    Hi,

      Please click on the link below to reset your password

      <a href="/forgotpassword/{token}> Click here </a>"""
