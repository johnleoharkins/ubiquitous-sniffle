from db import db
import sqlalchemy as sa


class PostModel(db.Model):
    __tablename__ = "posts"

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(120), nullable=False)
    body = db.Column(db.String(500), nullable=False)
    author = db.relationship("UserModel", back_populates="posts")
    author_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)

