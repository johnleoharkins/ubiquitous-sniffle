from flask_smorest.fields import Upload
from marshmallow import Schema, fields


class MultipartFileSchema(Schema):
    itemImageFile = Upload()


class PlainUserSchema(Schema):
    id = fields.Int(dump_only=True)
    username = fields.Str(required=True)


class PostSchema(Schema):
    id = fields.Int(dump_only=True)
    title = fields.Str(required=True, error_messages={"required": "Post 'title' is required."})
    body = fields.Str(required=True, error_messages={"required": "Post 'body' is required."})
    author_id = fields.Int()
    author = fields.Nested(PlainUserSchema(), dump_only=True)


class UserSchema(PlainUserSchema):
    password = fields.Str(required=True, load_only=True)
    posts = fields.List(fields.Nested(PostSchema(), dump_only=True))


class RestaurantMenuNewItemSchema(Schema):
    id = fields.Int(dump_only=True)
    category = fields.Str()
    name = fields.Str()
    price = fields.Float()
    description = fields.Str()
    itemImageFile = Upload()


class RestaurantMenuItemSchema(Schema):
    id = fields.Int(dump_only=True)
    category = fields.Str()
    name = fields.Str()
    price = fields.Float()
    description = fields.Str()
    imageURL = fields.Str()
