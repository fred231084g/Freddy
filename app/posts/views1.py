#This  file contains the API for Read only Posts
from flask import Blueprint, request, jsonify, make_response
from app.posts.models import Posts, PostsSchema
from flask_restful import Api, Resource
from sqlalchemy.exc import SQLAlchemyError
from marshmallow import ValidationError
from app.terms.models import Terms, TermsSchema

posts_read = Blueprint('posts_read', __name__)
schema = PostsSchema(strict=True)
termSchema = TermsSchema()
api = Api(posts_read)

class ReadPosts(Resource):

    def get(self):
        posts_query = Posts.query.filter_by(status="published").all()
        results = schema.dump(posts_query, many=True).data     
        return results

api.add_resource(ReadPosts, '.json')

class ReadPost(Resource):

    def get(self, id):
       
        post_query = Posts.query.get_or_404(id)
        result = schema.dump(post_query).data
        return result

api.add_resource(ReadPost, '/<int:id>.json')

class ReadTerms(Resource):

    def get(self):
      
        terms_query = Terms.query.all()
        result = termSchema.dump(terms_query, many=True).data
        return result

api.add_resource(ReadTerms, '/terms.json')
