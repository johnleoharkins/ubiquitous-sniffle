import os

import flask
from flask import redirect, url_for, app, send_from_directory
from flask_cors import CORS, cross_origin
from flask_smorest import Blueprint, abort
from flask.views import MethodView
from marshmallow.exceptions import ValidationError
from sqlalchemy import select
from werkzeug.utils import secure_filename


from db import db
from models import PostModel, UserModel
from schemas import PostSchema, MultipartFileSchema

from sqlalchemy.exc import SQLAlchemyError


# from flask_jwt_extended import jwt_required, get_jwt


blp = Blueprint("Posts", __name__, description="Operations on posts")

CORS(blp, origins='*', methods='DELETE, GET, HEAD, OPTIONS, PATCH, POST, PUT', allow_headers=['Content-Type', 'Content-Length', 'Accept', 'Accept-Encoding', 'Host', 'Connection', 'User-Agent'], send_wildcard=True, expose_headers=['Content-Type', 'Content-Length', 'Accept', 'Accept-Encoding', 'Host', 'Connection', 'User-Agent', 'Authorization'], vary_header=True)
# CORS(blp, )


@blp.route("/post/<int:post_id>")
class Post(MethodView):
    @blp.response(200, PostSchema)
    def get(self, post_id):
        post = PostModel.query.get_or_404(post_id)
        return post


@blp.route("/posts")
class PostsList(MethodView):
    @blp.response(200, PostSchema(many=True))
    def get(self):
        return PostModel.query.all()


@blp.route("/new-post")
class CreatePost(MethodView):
    @blp.arguments(PostSchema, location="json")
    @blp.response(201, PostSchema)
    def post(self, post_data):
        try:
            post = PostModel(**post_data)
        except ValidationError as err:
            print(err.messages)
            abort(400, message="ValidationError. An error occurred creating a model from the provided post data.")

        try:
            db.session.add(post)
            db.session.commit()
        except SQLAlchemyError:
            abort(500, message="An error occurred while adding new post.")
        return post


@blp.route("/upload")
class Upload(MethodView):
    @blp.arguments(MultipartFileSchema, location="files")
    @blp.response(201, MultipartFileSchema, content_type='multipart/form-data')
    def post(self, files):
        print(files)
        if files:
            # print(files)
            # mfs = MultipartFileSchema(files)
            # file_1 = mfs["file_1"]
            file_1 = files["file_1"]
            secureFilename = secure_filename(file_1.filename)
            print(os.path.abspath('..'))
            file_1.save(os.path.join('..', 'uploads/', secureFilename))
            response = flask.jsonify({'filename': secureFilename})
            # response.headers.add('Access-Control-Allow-Origin', '*')
            return response, 201
        else:
            # abort(500, message="An error occurred with upload.")
            # return flask.jsonify(success=False)
            return files


@blp.route("/uploads/<string:name>")
class GetUpload(MethodView):
    def get(self, name):
        return send_from_directory(os.path.join('..', 'uploads/'), name)
