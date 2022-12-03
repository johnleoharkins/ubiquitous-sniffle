import os

from flask import Flask, request, session, send_from_directory
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from flask_smorest import Api
from flask import g
from werkzeug.utils import secure_filename

from db import db
import logging

# lets SQLAlchemy know what models exist in our application
# they are db.Model instances, SQLAlchemy will look at their __tablename__
#                   and defined db.Column attributes to create the tables

from resources.user import blp as UserBlueprint
from resources.post import blp as PostBlueprint
from resources.restaurant import blp as RestaurantBlueprint

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger('HELLO WORLD')
# application factory function
def create_app(db_url=None):
    # logging.basicConfig(filename='record.log', level=logging.DEBUG)
    app = Flask(__name__)

    UPLOAD_FOLDER = '../uploads'
    ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}

    # app config things
    app.config["PROPAGATE_EXCEPTIONS"] = True
    app.config["API_TITLE"] = "project: settle-regulation-torch REST API"
    app.config["API_VERSION"] = "v1"
    app.config["OPENAPI_VERSION"] = "3.0.3"
    app.config["OPENAPI_URL_PREFIX"] = "/"
    app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
    app.config['MAX_CONTENT_LENGTH'] = 16 * 1000 * 1000
    # use swagger for api documentation
    app.config["OPENAPI_SWAGGER_UI_PATH"] = "/swagger-ui"
    app.config["OPENAPI_SWAGGER_UI_URL"] = "https://cdn.jsdelivr.net/npm/swagger-ui-dist/"
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///data.db"
    # app.config["SQLALCHEMY_DATABASE_URI"] = db_url or os.getenv("DATABASE_URL", "sqlite:///data.db")

    # connect sqlalchemy
    # db.init_app(app)

    # migrate = Migrate(app, db)

    with app.app_context():
        db.init_app(app)
        db.create_all()

    # connect flask-smorest extension to flask application
    api = Api(app)


    # jwt config and instantiation
    app.config["JWT_SECRET_KEY"] = "john"
    app.secret_key = os.urandom(24)
    jwt = JWTManager(app)
    @app.route('/restaurant/item-image/<name>')
    def download_item_image_file(name):
        path = f'menu-item-images/{name}'
        return send_from_directory(app.config["UPLOAD_FOLDER"], path)
        app.add_url_rule(
            "/restaurant/item-image/<name>", endpoint="download_item_image_file", build_only=True
        )

    # register blueprints
    api.register_blueprint(UserBlueprint)
    api.register_blueprint(PostBlueprint)
    api.register_blueprint(RestaurantBlueprint)


    @app.route('/upload2', methods=['POST'])
    def fileUpload():
        target = os.path.join(app.config['UPLOAD_FOLDER'], 'test')
        if not os.path.isdir(target):
            os.mkdir(target)
        logger.info(f"welcome to upload {request.files}")
        file = request.files['file_1']
        filename = secure_filename(file.filename)
        destination = "/".join([target, filename])
        file.save(destination)
        session['uploadFilePath'] = destination
        response = "Whatever you wish too return"
        return response
    CORS(app, origins='*', methods='DELETE, GET, HEAD, OPTIONS, PATCH, POST, PUT',
         allow_headers=['Content-Type', 'Content-Length', 'Accept', 'Accept-Encoding', 'Host', 'Connection',
                        'User-Agent'], send_wildcard=True,
         expose_headers=['Content-Type', 'Content-Length', 'Accept', 'Accept-Encoding', 'Host', 'Connection',
                         'User-Agent', 'Authorization'], vary_header=True)


    return app

