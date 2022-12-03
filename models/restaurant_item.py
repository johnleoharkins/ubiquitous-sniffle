from db import db


class RestaurantItemModel(db.Model):
    __tablename__ = "restaurant-item"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50))
    category = db.Column(db.String(20))
    price = db.Column(db.Float)
    description = db.Column(db.String(310))
    imageURL = db.Column(db.String(80))
