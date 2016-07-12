#!/bin/bash




#TESTS
#Tests for terms
protractor  app/templates/terms/conf.js  &&
python app/terms/test_terms.py
#End Tests for terms
#Tests for posts
protractor  app/templates/posts/conf.js  &&
python app/posts/test_posts.py
#End Tests for posts
#Tests for comments
protractor  app/templates/comments/conf.js  &&
python app/comments/test_comments.py
#End Tests for comments

