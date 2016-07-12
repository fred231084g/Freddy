# http://werkzeug.pocoo.org/docs/0.11/test/#werkzeug.test.Client
# http://flask.pocoo.org/docs/0.10/api/#test-client

import unittest
import os
import sys
import json

# Add app path to module path
sys.path.append(os.path.dirname(os.path.realpath(__file__).rsplit('/', 2)[0]))
from app import create_app
#from app.posts.models import Posts


app = create_app('config')
add_data = """{
  "data": {
    "attributes":

    {"excerpt": "How to build CRUD app with Python, Flask, SQLAlchemy and MySQL. Som reand456989@#$%^%> <html/>", "type": "test string", "comments": "test string", "content": "How to build CRUD app with Python, Flask, SQLAlchemy and MySQL. Som reand456989@#$%^%> <html/>", "title": "How to build CRUD app with Python, Flask, SQLAlchemy and MySQL. Som reand456989@#$%^%> <html/>", "terms": "test string", "parent": 35678, "date": "2015-12-22T03:12:58.019077+00:00", "status": "test string", "modified_gmt": "2015-12-22T03:12:58.019077+00:00", "author": "test string", "modified": "2015-12-22T03:12:58.019077+00:00", "slug": "test string", "date_gmt": "2015-12-22T03:12:58.019077+00:00"}
         ,

    "type": "posts"
  }

}"""

update_data = """{
  "data": {
    "attributes":

        {"excerpt": "How to build CRUD app with Python, Flask, SQLAlchemy and MySQL. Som reand456989@#$%^%> <html/>", "type": "test string", "comments": "test string", "content": "How to build CRUD app with Python, Flask, SQLAlchemy and MySQL. Som reand456989@#$%^%> <html/>", "title": "How to build CRUD app with Python, Flask, SQLAlchemy and MySQL. Som reand456989@#$%^%> <html/>", "terms": "test string", "parent": 35678, "date": "2015-12-22T03:12:58.019077+00:00", "status": "test string", "modified_gmt": "2015-12-22T03:12:58.019077+00:00", "author": "test string", "modified": "2015-12-22T03:12:58.019077+00:00", "slug": "test string", "date_gmt": "2015-12-22T03:12:58.019077+00:00"},
    "type": "posts"
  }

}"""


class TestPosts(unittest.TestCase):

    def setUp(self):
        self.app = app.test_client()

    def test_01_add(self):

        rv = self.app.post('/api/v1/posts.json', data=add_data,
                           content_type="application/json")
        assert rv.status_code == 201

    def test_02_read_update(self):
        request = self.app.get('/api/v1/posts.json')
        dict = json.loads(request.data.decode('utf-8'))
        id = dict['data'][0]['id']
        rv = self.app.patch('/api/v1/posts/{}.json'.format(id),
                            data=update_data, content_type="application/json")
        assert rv.status_code == 200

    def test_03_delete(self):
        request = self.app.get('/api/v1/posts.json')
        dict = json.loads(request.data.decode('utf-8'))
        id = dict['data'][0]['id']
        rv = self.app.delete('/api/v1/posts/{}.json'.format(id))
        assert rv.status_code == 204

if __name__ == '__main__':
    unittest.main()
