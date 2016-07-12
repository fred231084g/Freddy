import unittest
from app import app

#http://flask.pocoo.org/docs/0.10/testing/
#http://www.diveintopython3.net/unit-testing.html

class TestBlog(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()
     
    def test_index(self): 
      self.app = app.test_client()    
      rv = self.app.get('/')
      assert 'Read More' in rv.data.decode('utf-8')
      
    def login(self, email, password):
        return self.app.post('/login', data=dict(email=email, password=password), follow_redirects=True)

    def logout(self):
        return self.app.get('/logout', follow_redirects=True)
        
    def test_login_logout(self):
        rv = self.login('leo@leog.in', 'qwedsa')
        #print(rv.data.decode('utf-8'))
        assert 'Posts' in rv.data.decode('utf-8')
        rv = self.logout()
        assert 'Sign In' in rv.data.decode('utf-8')
        
    def test_terms(self):
        self.login('leo@leog.in', 'qwedsa')
        rv = self.app.post('/terms/add', data=dict(
        name = 'test tag1',
        slug = 'test- case',
        description = 'test description',
        taxonomy = 'tag',
        parent = '0'), follow_redirects=True)
        assert 'Add was successful' in rv.data.decode('utf-8')
        
        self.login('leo@leog.in', 'qwedsa')
        rv = self.app.post('/terms/add', data=dict(
        name = 'test category',
        slug = 'test- case',
        description = 'test description',
        taxonomy = 'category',
        parent = '0'), follow_redirects=True)
        assert 'Add was successful' in rv.data.decode('utf-8')
        
        
    
      
if __name__ == '__main__':
    unittest.main()