import os

from flask import request, session, url_for, current_app
from flask_jwt_extended import create_access_token, create_refresh_token
from flask_smorest import Blueprint, abort
from flask.views import MethodView
from passlib.hash import pbkdf2_sha256
from flask_cors import CORS
from sqlalchemy.exc import SQLAlchemyError
from werkzeug.utils import secure_filename

import app
# from app import logger
from models import UserModel, RestaurantItemModel
from schemas import UserSchema, RestaurantMenuNewItemSchema, RestaurantMenuItemSchema

from db import db

# from flask_jwt_extended import jwt_required, get_jwt


blp = Blueprint("Restaurant", __name__, description="Operations on restaurants")

# CORS(blp)

@blp.route("/restaurant/menu" )
class RestaurantMenu(MethodView):
    @blp.response(200, RestaurantMenuItemSchema(many=True))
    def get(self):
        return RestaurantItemModel.query.all()





@blp.route("/restaurant/new-item")
class RestaurantMenuNewItem(MethodView):
    @blp.arguments(RestaurantMenuNewItemSchema, location='files')
    @blp.response(201, RestaurantMenuItemSchema(many=True))
    def post(self, file_upload):
        new_item_data = request.form
        print(f"new_item_data after deserialization... {new_item_data} ")
        # logger.info(f"welcome to /new-item upload. request.files: {request.files}")

        target = os.path.join(current_app.config['UPLOAD_FOLDER'], 'menu-item-images')
        if not os.path.isdir(target):
            os.mkdir(target)
        file = file_upload['itemImageFile']
        if file.filename == '':
            abort(400, message="Invalid filename. Empty filename. Please select a file")
        filename = secure_filename(file.filename)
        destination = "/".join([target, filename])
        file.save(destination)
        session['uploadFilePath'] = destination
        item_image_url = url_for('download_item_image_file', name=filename)

        new_item_model = RestaurantItemModel(
            category=new_item_data["category"],
            name=new_item_data["name"],
            price=new_item_data["price"],
            description=new_item_data["description"],
            imageURL=item_image_url
        )
        try:
            db.session.add(new_item_model)
            db.session.commit()
        except SQLAlchemyError:
            abort(500, message="An error occured while adding new menu item.")
        return RestaurantItemModel.query.all(), 201


