Freddy is a Blog Engine Built using Python 3, Flask and Angularjs.

### Features

- SEO friendly URL's
- Built in Google Analytics Support
- Client side routing for Speedier loading of Web Pages.
- JSON Token based Authentication with ACL's
- Builtin Social Media Support with Facebook comments
- Tagging and Categories
- Image Gallery


### Installation

    git clone
    pip install -r requirements
    #Add your DB configuration in config.py
    python db.py db init
    python db.py db migrate
    python db.py db upgrade
    python run.py
    
You should be able to access your website at http://localhost:5000 and admin interface at ttp://localhost:5000/admin. There is no default user you will need to Sign Up to creat one.

![](http://i.imgur.com/rxFMACc.png)

Demo at https://freddy-flask.herokuapp.com/

Built using https://github.com/Leo-G/Flask-Scaffold/


