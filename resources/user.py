from flask_jwt_extended import create_access_token, create_refresh_token
from flask_smorest import Blueprint, abort
from flask.views import MethodView
from passlib.hash import pbkdf2_sha256
from flask_cors import CORS

from models import UserModel
from schemas import UserSchema

from db import db

# from flask_jwt_extended import jwt_required, get_jwt


blp = Blueprint("Users", __name__, description="Operations on users")

CORS(blp)


@blp.route("/register")
class UserRegistration(MethodView):
    @blp.arguments(UserSchema)
    @blp.response(201)
    def post(self, user_data):
        # newUser = UserModel(**user_data)
        if UserModel.query.filter(UserModel.username == user_data["username"]).first():
            abort(409, message="A user with that username already exists.")

        user = UserModel(
            username=user_data["username"],
            password=pbkdf2_sha256.hash(user_data["password"])
        )
        db.session.add(user)
        db.session.commit()

        return {"message": "User created successfully."}, 201


@blp.route("/login")
class UserLogin(MethodView):
    @blp.arguments(UserSchema)
    def post(self, user_data):
        user = UserModel.query.filter(
            UserModel.username == user_data["username"]
        ).first()

        # check if user exists and if hashed passwords are equivalent
        if user and pbkdf2_sha256.verify(user_data["password"], user.password):
            access_token = create_access_token(identity=user.id, fresh=True)
            refresh_token = create_refresh_token(identity=user.id)
            return {"access_token": access_token, "refresh_token": refresh_token, "username": user.username, "user_id": user.id}

        abort(401, message="Invalid credentials.")


@blp.route("/logout")
class UserLogout(MethodView):
    def post(self):
        # jti = get_jwt()["jti"]
        # BLOCKLIST.add(jti)
        return {"message": "Successfully logged out."}

