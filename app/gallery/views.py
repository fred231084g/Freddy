import os
from flask import Blueprint, request, jsonify, make_response
from app.gallery.models import Gallery, GallerySchema
from flask_restful import Api
from app.baseviews import Resource
from app.basemodels import db
from sqlalchemy.exc import SQLAlchemyError
from marshmallow import ValidationError
from werkzeug import secure_filename
from config import UPLOAD_FOLDER


gallery = Blueprint('gallery', __name__)
# http://marshmallow.readthedocs.org/en/latest/quickstart.html#declaring-schemas
# https://github.com/marshmallow-code/marshmallow-jsonapi
schema = GallerySchema(strict=True)
api = Api(gallery)
ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'])


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS

# Gallery


class CreateListFiles(Resource):
    """http://jsonapi.org/format/#fetching
    A server MUST respond to a successful request to fetch an individual resource or resource collection with a 200 OK response.
    A server MUST respond with 404 Not Found when processing a request to fetch a single resource that does not exist, except when the request warrants a 200 OK response with null as the primary data (as described above)
    a self link as part of the top-level links object"""

    def get(self):
        files_query = Gallery.query.all()
        results = schema.dump(files_query, many=True).data
        return results

    """http://jsonapi.org/format/#crud
    A resource can be created by sending a POST request to a URL that represents a collection of gallery. The request MUST include a single resource object as primary data. The resource object MUST contain at least a type member.
    If a POST request did not include a Client-Generated ID and the requested resource has been created successfully, the server MUST return a 201 Created status code"""

    def post(self):

        try:
            file = request.files['path']
            if file and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                file_path = os.path.join(
                    'app/templates', UPLOAD_FOLDER, filename)
                file.save(file_path)
            gallery = Gallery(request.form['name'], request.form['tags'],  os.path.join(
                UPLOAD_FOLDER, filename), request.form['category'])
            gallery.add(gallery)
            query = Gallery.query.get(gallery.id)
            results = schema.dump(query).data
            return results, 201

        except ValidationError as err:
            resp = jsonify({"error": err.messages})
            resp.status_code = 403
            return resp

        except SQLAlchemyError as e:
            db.session.rollback()
            resp = jsonify({"error": str(e)})
            resp.status_code = 403
            return resp


class GetUpdateDeleteFile(Resource):

    """http://jsonapi.org/format/#fetching
    A server MUST respond to a successful request to fetch an individual resource or resource collection with a 200 OK response.
    A server MUST respond with 404 Not Found when processing a request to fetch a single resource that does not exist, except when the request warrants a 200 OK response with null as the primary data (as described above)
    a self link as part of the top-level links object"""

    def get(self, id):
        file_query = Gallery.query.get_or_404(id)
        result = schema.dump(file_query).data
        return result

    """http://jsonapi.org/format/#crud-updating"""

    def patch(self, id):
        gallery = Gallery.query.get_or_404(id)
        print(request.form)
        print(request.files['path'])
        try:
            # Save file
            file = request.files['path']
            if file and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                file_path = os.path.join(
                    'app/templates', UPLOAD_FOLDER, filename)
                file.save(file_path)
            gallery.path = os.path.join(UPLOAD_FOLDER, filename)

            # Save form fields
            form = request.form
            for key, value in form.items():
                setattr(gallery, key, value)

            gallery.update()
            return self.get(id)

        except ValidationError as err:
            resp = jsonify({"error": err.messages})
            resp.status_code = 401
            return resp

        except SQLAlchemyError as e:
            db.session.rollback()
            resp = jsonify({"error": str(e)})
            resp.status_code = 401
            return resp

    # http://jsonapi.org/format/#crud-deleting
    # A server MUST return a 204 No Content status code if a deletion request
    # is successful and no content is returned.
    def delete(self, id):
        gallery = Gallery.query.get_or_404(id)
        try:
            delete = gallery.delete(gallery)
            response = make_response()
            response.status_code = 204
            return response

        except SQLAlchemyError as e:
            db.session.rollback()
            resp = jsonify({"error": str(e)})
            resp.status_code = 401
            return resp


api.add_resource(CreateListFiles, '.json')
api.add_resource(GetUpdateDeleteFile, '/<int:id>.json')
